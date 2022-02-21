import io
import logging
import re
from typing import List, Tuple

import pdf2image
import pyheif
import pyzbar.pyzbar
from PIL import Image
from django.conf import settings
from django.template.loader import render_to_string
from google.protobuf.message import DecodeError
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, BotCommand
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, Updater, \
    Dispatcher

from app_telegram.models import WarningSubscription
from location.models import Location
from warning.models import TraceTimeIntervalWarning, CheckInProtectedReport, CheckInRecord, TraceWarningPackage

logger = logging.getLogger(__name__)


def read_qr_code(images: List) -> List[str]:
    codes = []
    for image in images:
        codes += [code.data for code in pyzbar.pyzbar.decode(image, symbols=[pyzbar.pyzbar.ZBarSymbol.QRCODE])]

    return [code.decode("ascii") for code in codes]


def send_location_data(update: Update, location: Location):
    try:
        update.message.reply_html(
            render_to_string("telegram/location_data.html", {'payload': location.to_object(), 'location': location}),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Subscribe", callback_data=f"subscribe {location.uuid}")],
                [InlineKeyboardButton("Show Warnings", callback_data=f"get_warnings {location.uuid}")],
                [InlineKeyboardButton("Check-In", url=location.url)],
            ])
        )
    except DecodeError:
        update.message.reply_text("Error: couldn't decode CWA payload")


def process_qr_code_images(update: Update, images: List):
    urls = read_qr_code(images)

    if len(urls) == 0:
        update.effective_chat.send_message("No QR code found")

    process_urls(update, urls)


def process_urls(update: Update, urls: List[str]):
    # filter out duplicates
    urls = list(dict.fromkeys(urls))

    for url in urls:
        try:
            Location.decode_payload(url)
        except Exception as e:
            update.effective_chat.send_message(
                text=f"URL could not be parsed:\n{e}",
                disable_web_page_preview=True,
            )
            continue

        location, _ = Location.objects.get_or_create(url=url)
        send_location_data(update, location)


def on_start(update: Update, context: CallbackContext):
    update.message.reply_text(
        f'Hello {update.effective_user.first_name}!'
        f'\n'
        f'I am the unofficial Corona-Warn-App Warning Bot!\n'
        f'Just send me a CWA QR-code and I can show you recent warnings for that code.'
        f'\n'
        f'You can also subscribe for future warnings.'
        f'\n\n'
        f'Hint: If the QR-code is not recognized by me, try sending it in a higher resolution and without compression.'
        f'\n'
        f'Another alternative is sending the URL from the code as text.'
        f'\n\n'
        f'Stay safe!')
    logger.warning(f'New User: {update.effective_user.username}')


def on_photo(update: Update, context: CallbackContext):
    process_qr_code_images(
        update,
        [Image.open(io.BytesIO(p.get_file().download_as_bytearray())) for p in update.message.photo]
    )


def on_document(update: Update, context: CallbackContext):
    if update.message.document:
        doc = update.message.document

        if doc.mime_type == "application/pdf":
            process_qr_code_images(
                update,
                pdf2image.convert_from_bytes(doc.get_file().download_as_bytearray()),
            )
        elif doc.mime_type in ["image/jpeg", "image/png"]:
            process_qr_code_images(
                update,
                [Image.open(io.BytesIO(doc.get_file().download_as_bytearray()))]
            )
        elif doc.mime_type == "image/heic":
            heif_file = pyheif.read(io.BytesIO(doc.get_file().download_as_bytearray()))
            image = Image.frombytes(mode=heif_file.mode, size=heif_file.size, data=heif_file.data)
            process_qr_code_images(
                update,
                [image],
            )
        else:
            update.message.reply_text(f'Mime-Type "{doc.mime_type}" not supported!')
            logger.warning(f'Mime-Type "{doc.mime_type}" not supported!')


def on_text(update: Update, context: CallbackContext):
    matches = re.findall(r"(http[s]?://[^\s$]+)", update.message.text)
    process_urls(update, matches)


def on_callback(update: Update, context: CallbackContext):
    cb_data: str = update.callback_query.data

    if cb_data:
        command, *args = cb_data.split(" ")

        if command == "subscribe" and len(args) == 1:
            location = Location.objects.get(uuid=args[0])
            subscription, created = WarningSubscription.objects.get_or_create(
                location=location,
                chat=update.effective_chat.id,
            )
            if created:
                update.effective_chat.send_message("Subscription created!")
            else:
                update.effective_chat.send_message("Subscription renewed!")
        elif command == "get_warnings" and len(args) == 1:
            location = Location.objects.get(uuid=args[0])

            check_in_records: List[Tuple[TraceWarningPackage, CheckInRecord]] = []

            for item in TraceTimeIntervalWarning.objects.filter(location_id_hash=location.location_id_hash):
                check_in_records.append((item.package, item.check_in_record))

            for item in CheckInProtectedReport.objects.filter(location_id_hash=location.location_id_hash):
                check_in_records.append((item.package, item.decrypt(location.location_id)))

            if len(check_in_records) == 0:
                update.effective_chat.send_message("No warnings found.")
            else:
                check_in_records.sort(key=lambda r: r[1].start_interval_number)

                for package, record in check_in_records:
                    try:
                        location_description = location.to_object().locationData.description
                        update.effective_chat.send_message(
                            text=render_to_string("telegram/check_in_record.html", {
                                'record': record,
                                'location': location_description,
                                'package': package,
                            }),
                            parse_mode="HTML",
                        )
                    except DecodeError:
                        continue
        else:
            update.effective_chat.send_message("Error: %s" % update.callback_query.data)


def on_get_subscriptions(update: Update, context: CallbackContext):
    for subscription in WarningSubscription.objects.filter(chat=update.effective_chat.id):
        send_location_data(update, subscription.location)


def get_updater() -> Updater:
    return Updater(settings.TELEGRAM_TOKEN)


def get_bot() -> Bot:
    return get_updater().bot


def get_username_from_chat_id(chat_id, bot: Bot = None) -> str:
    if not bot:
        bot = get_bot()

    return bot.get_chat(chat_id).username


def run():
    logger.info("Loading handlers for telegram bot")

    updater = get_updater()
    bot: Bot = updater.bot
    dispatcher: Dispatcher = updater.dispatcher
    bot.setMyCommands([
        BotCommand("start", "Show welcome message"),
        BotCommand("subscriptions", "Show subscriptions"),
    ])

    dispatcher.add_handler(CommandHandler("start", on_start))
    dispatcher.add_handler(CommandHandler("subscriptions", on_get_subscriptions))
    dispatcher.add_handler(MessageHandler(Filters.text, on_text))
    dispatcher.add_handler(MessageHandler(Filters.photo, on_photo))
    dispatcher.add_handler(MessageHandler(Filters.document, on_document))
    dispatcher.add_handler(CallbackQueryHandler(on_callback))

    # TODO: Error handler
    # dispatcher.add_error_handler(error)

    updater.start_polling()
    logger.warning("Running")
    updater.idle()
