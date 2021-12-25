import base64
import hashlib

from django.db import models
import urllib.parse

from django.utils.translation import gettext as _

from proto.cwa_location_pb2 import QRCodePayload


class Location(models.Model):
    url = models.URLField(
        unique=True,
        max_length=1024,
        verbose_name=_("URL"),
        help_text=_("The url which is encoded in the QRCode"),
    )

    location_id_hash = models.BinaryField(
        verbose_name=_("Location ID Hash"),
        help_text=_("SHA256 hash of the CWA location ID")
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

    def _get_location_id_hash(self) -> bytes:
        return hashlib.sha256(self.location_id).digest()

    def save(self, *args, **kwargs):
        # calculate location_id_hash automatically before save
        self.location_id_hash = self._get_location_id_hash()
        super(Location, self).save(*args, **kwargs)

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
