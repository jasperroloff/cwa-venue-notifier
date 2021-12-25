from django.core.management.base import BaseCommand
from tabulate import tabulate

import app_telegram.telegram

from app_telegram.models import WarningSubscription

DIRNAME = "packages"


class Command(BaseCommand):
    help = 'Show subscriptions (id, chat_id, username, location_id, description)'

    def handle(self, *args, **options):
        rows = []
        bot = app_telegram.telegram.get_bot()
        for subscription in WarningSubscription.objects.all():
            rows.append([
                subscription.pk,
                subscription.chat,
                app_telegram.telegram.get_username_from_chat_id(subscription.chat, bot),
                subscription.location.pk,
                subscription.location.to_object().locationData.description,
            ])

        print(tabulate(rows, headers=['ID', 'Chat ID', 'Username', 'Location ID', 'Description'], tablefmt='orgtbl'))
