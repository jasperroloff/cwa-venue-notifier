import io
import logging
from typing import List
from typing.io import IO

import pyheif
import pyzbar.pyzbar
from PIL import Image
import pdf2image


logger = logging.getLogger(__name__)


class FileToImagesError(Exception):
    pass


def bytes_to_images(mime_type, file_content: bytes) -> List[Image.Image]:
    if mime_type == "application/pdf":
        return pdf2image.convert_from_bytes(file_content)
    elif mime_type in ["image/jpeg", "image/png"]:
        return [_photo_to_image(io.BytesIO(file_content))]
    elif mime_type == "image/heic":
        return [_heif_to_image(io.BytesIO(file_content))]
    else:
        # TODO
        logger.warning(f'Mime-Type "{mime_type}" not supported!')
        raise FileToImagesError(f'Mime-Type "{mime_type}" not supported!')


def file_to_images(mime_type, file: IO) -> List[Image.Image]:
    if mime_type == "application/pdf":
        return pdf2image.convert_from_path(file.name)
    elif mime_type in ["image/jpeg", "image/png"]:
        return [_photo_to_image(file)]
    elif mime_type == "image/heic":
        return [_photo_to_image(file)]
    else:
        # TODO
        logger.warning(f'Mime-Type "{mime_type}" not supported!')
        raise FileToImagesError(f'Mime-Type "{mime_type}" not supported!')


def _photo_to_image(file) -> Image.Image:
    return Image.open(file)


def _heif_to_image(file) -> Image.Image:
    heif_file = pyheif.read(file)
    image = Image.frombytes(mode=heif_file.mode, size=heif_file.size, data=heif_file.data)
    return image


def process_qr_code_images(images: List) -> List[str]:
    urls = []

    for image in images:
        urls += read_qr_code(image)

    return urls


def read_qr_code(image) -> List[str]:
    codes = [code.data for code in pyzbar.pyzbar.decode(image, symbols=[pyzbar.pyzbar.ZBarSymbol.QRCODE])]
    return [code.decode("ascii") for code in codes]
