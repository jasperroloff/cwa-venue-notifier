import base64
import hashlib
import uuid

from django.core.exceptions import ValidationError
from django.db import models
import urllib.parse

from django.urls import reverse
from django.utils.translation import gettext as _
from google.protobuf.message import DecodeError

from proto.cwa_location_pb2 import QRCodePayload


class PayloadDecodeError(Exception):
    pass


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

    def __init__(self, *args, **kwargs):
        super(Location, self).__init__(*args, **kwargs)

        if 'url' in kwargs.keys():
            self.clean()

    def get_absolute_url(self):
        if self.pk:
            return reverse('location-details', kwargs={'uuid': self.uuid})
        else:
            return reverse('location-details', kwargs={'url': self.url})

    @property
    def provider(self) -> str:
        return urllib.parse.urlparse(self.url).hostname

    @property
    def payload(self) -> bytes:
        return Location.get_payload_from_url(self.url)

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
    def extract_payload_from_url(cls, url: str) -> str:
        cwa_payload = urllib.parse.urlparse(url).fragment

        if not cwa_payload:
            raise PayloadDecodeError("unknown url format: %s" % url)

        if "/CWA1/" in cwa_payload:
            cwa_payload = cwa_payload.split("/CWA1/")[1]

        return cwa_payload

    @classmethod
    def decode_payload(cls, cwa_payload: str) -> bytes:
        try:
            cwa_payload_b = cwa_payload.encode('ascii')
            cwa_payload_b += b"=" * ((4 - len(cwa_payload_b) % 4) % 4)
            cwa_payload = cwa_payload_b.decode('ascii')
            decoded = base64.urlsafe_b64decode(cwa_payload)
        except:
            raise PayloadDecodeError("error decoding payload from url")

        if not decoded:
            raise PayloadDecodeError("CWA payload is empty")

        return decoded

    @classmethod
    def get_payload_from_url(cls, url: str) -> bytes:
        cwa_payload = Location.extract_payload_from_url(url)
        return Location.decode_payload(cwa_payload)

    @classmethod
    def get_by_url(cls, url: str) -> "Location":
        Location.get_payload_from_url(url)
        location = Location(url=url)
        # try to find location in DB by searching by location id hash
        try:
            return Location.objects.get(location_id_hash=location.location_id_hash)
        except Location.DoesNotExist:
            return location
