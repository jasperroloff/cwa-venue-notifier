import base64
import hashlib
import uuid

from django.core.exceptions import ValidationError
from django.db import models
import urllib.parse

from django.utils.translation import gettext as _
from google.protobuf.message import DecodeError

from proto.cwa_location_pb2 import QRCodePayload


class Location(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name=_("UUID"),
        help_text=_("Used as unique identifier to clients"),
    )

    url = models.URLField(
        unique=True,
        max_length=1024,
        verbose_name=_("URL"),
        help_text=_("The url which is encoded in the QRCode"),
        # editable=False,
    )

    location_id_hash = models.BinaryField(
        verbose_name=_("Location ID Hash"),
        help_text=_("SHA256 hash of the CWA location ID"),
        unique=True,
        editable=False,
    )

    @property
    def provider(self) -> str:
        return urllib.parse.urlparse(self.url).hostname

    @property
    def payload(self) -> bytes:
        return Location.decode_payload(self.url)

    def to_object(self) -> QRCodePayload:
        return QRCodePayload.FromString(self.payload)

    @property
    def location_id(self) -> bytes:
        return hashlib.sha256("CWA-GUID".encode('ascii') + self.payload).digest()

    @property
    def description(self) -> str:
        try:
            return self.to_object().locationData.description
        except DecodeError:
            return "(error)"

    @property
    def address(self) -> str:
        try:
            return self.to_object().locationData.address
        except DecodeError:
            return "(error)"

    def __str__(self):
        return f"{self.description} ({self.provider})"

    def _get_location_id_hash(self) -> bytes:
        return hashlib.sha256(self.location_id).digest()

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Location, self).save(*args, **kwargs)

    def clean(self):
        try:
            # calculate location_id_hash automatically before save
            self.location_id_hash = self._get_location_id_hash()
        except Exception as e:
            raise ValidationError(e)

    @classmethod
    def decode_payload(cls, url: str) -> bytes:
        cwa_payload = urllib.parse.urlparse(url).fragment

        if not cwa_payload:
            raise Exception("unknown url format: %s" % url)

        if "/CWA1/" in cwa_payload:
            cwa_payload = cwa_payload.split("/CWA1/")[1]

        try:
            cwa_payload_b = cwa_payload.encode('ascii')
            cwa_payload_b += b"=" * ((4 - len(cwa_payload_b) % 4) % 4)
            cwa_payload = cwa_payload_b.decode('ascii')
            decoded = base64.urlsafe_b64decode(cwa_payload)
        except:
            raise Exception("error decoding payload from url: %s" % url)

        if not decoded:
            raise Exception("CWA payload is empty")

        return decoded
