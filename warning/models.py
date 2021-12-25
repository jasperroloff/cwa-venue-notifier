import datetime
import hashlib
import hmac
import os

from django.conf import settings
from django.db import models

from django.utils.translation import gettext as _

from Crypto.Cipher import AES
from proto import trace_warning_pb2


class TraceWarningPackage(models.Model):
    api_version = models.IntegerField(
        verbose_name=_("API Version"),
        help_text=_("Version of the API"),
    )
    interval_number = models.BigIntegerField(
        verbose_name=_("Interval Number"),
        help_text=_("Interval in 10 minute steps since UNIX epoch"),
    )
    region = models.CharField(
        max_length=2,
        verbose_name=_("Region"),
        help_text=_("For example 'DE'"),
    )

    imported_at = models.DateTimeField(
        null=True,
    )

    @property
    def filename(self) -> str:
        return f"{self.interval_number}_{self.region}_v{self.api_version}.zip"

    @property
    def filepath(self):
        return os.path.join(settings.PACKAGES_DIR, self.filename)

    def __str__(self):
        return f"{self.region}/v{self.api_version}/{self.interval_number}"

    class Meta:
        unique_together = ("api_version", "interval_number", "region")
        ordering = ['-interval_number']


class CheckInRecordType:
    TraceTimeIntervalWarning = "TraceTimeIntervalWarning"
    CheckInProtectedReport = "CheckInProtectedReport"

    choices = (
        (TraceTimeIntervalWarning, "TraceTimeIntervalWarning"),
        (CheckInProtectedReport, "CheckInProtectedReport"),
    )


class CheckInRecord:
    start_interval_number = models.BigIntegerField(
        verbose_name=_("Start interval number"),
        help_text=_("Start interval in 10 minute steps since UNIX epoch"),
    )
    period = models.BigIntegerField(
        verbose_name=_("Period"),
        help_text=_("Warning duration in 10 minute steps"),
    )
    transmission_risk_level = models.IntegerField(
        verbose_name=_("Transmission Risk Level"),
        # help_text=_(""),
    )
    type = models.CharField(choices=CheckInRecordType.choices)

    @property
    def start(self) -> datetime.datetime:
        return datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)\
               + datetime.timedelta(minutes=self.start_interval_number * 10)

    @property
    def end(self) -> datetime.datetime:
        return self.start + self.duration

    @property
    def duration(self) -> datetime.timedelta:
        return datetime.timedelta(minutes=10 * self.period)


class TraceTimeIntervalWarning(models.Model):
    package = models.ForeignKey(
        TraceWarningPackage,
        on_delete=models.CASCADE,
        verbose_name=_("Package"),
        help_text=_("The warning package, where this time interval warning comes from"),
    )
    position = models.IntegerField(
        # verbose_name=_("Location ID Hash"),
        # help_text=_("SHA256 hash of the location ID"),
    )
    location_id_hash = models.BinaryField(
        verbose_name=_("Location ID Hash"),
        help_text=_("SHA256 hash of the location ID"),
    )
    start_interval_number = models.BigIntegerField(
        verbose_name=_("Start interval number"),
        help_text=_("Start interval in 10 minute steps since UNIX epoch"),
    )
    period = models.BigIntegerField(
        verbose_name=_("Period"),
        help_text=_("Warning duration in 10 minute steps"),
    )
    transmission_risk_level = models.BigIntegerField(
        verbose_name=_("Transmission Risk Level"),
        # help_text=_(""),
    )

    @property
    def check_in_record(self) -> CheckInRecord:
        result = CheckInRecord()
        result.period = self.period
        result.start_interval_number = self.start_interval_number
        result.transmission_risk_level = self.transmission_risk_level
        result.type = CheckInRecordType.TraceTimeIntervalWarning
        return result

    class Meta:
        unique_together = ("package", "position")


class CheckInProtectedReport(models.Model):
    package = models.ForeignKey(
        TraceWarningPackage,
        on_delete=models.CASCADE,
        verbose_name=_("Package"),
        help_text=_("The warning package, where this protected check-in report comes from"),
    )
    position = models.IntegerField(
        # verbose_name=_("Location ID Hash"),
        # help_text=_("SHA256 hash of the location ID"),
    )
    location_id_hash: bytes = models.BinaryField(
        verbose_name=_("Location ID Hash"),
        help_text=_("SHA256 hash of the location ID"),
    )
    iv: bytes = models.BinaryField(
        verbose_name=_("IV"),
        # help_text=_(""),
    )
    encrypted_check_in_record: bytes = models.BinaryField(
        verbose_name=_("Encrypted Check-In Record"),
        # help_text=_(""),
    )
    mac: bytes = models.BinaryField(
        verbose_name=_("MAC"),
        # help_text=_(""),
    )

    def decrypt(self, location_id: bytes) -> CheckInRecord:
        mac_key = hashlib.sha256(settings.CWA_MAC_KEY + location_id).digest()

        iv: bytes = self.iv.tobytes() if isinstance(self.iv, memoryview) else self.iv
        enc_record: bytes = self.encrypted_check_in_record.tobytes() if isinstance(self.encrypted_check_in_record, memoryview) else self.encrypted_check_in_record
        mac: bytes = self.mac.tobytes() if isinstance(self.mac, memoryview) else self.mac

        calculated_mac = hmac.new(mac_key, b"" + iv + enc_record, digestmod=hashlib.sha256).digest()

        if not mac == calculated_mac:
            raise Exception("MACs do not match!")

        encryption_key = hashlib.sha256(settings.CWA_ENCRYPTION_KEY + location_id).digest()

        # "AES/CBC/PKCS5Padding"
        cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(enc_record)

        unpad = lambda s: s[0:-int(s[-1])]
        obj = trace_warning_pb2.CheckInRecord.FromString(unpad(decrypted))

        result = CheckInRecord()
        result.period = obj.period
        result.start_interval_number = obj.startIntervalNumber
        result.transmission_risk_level = obj.transmissionRiskLevel
        result.type = CheckInRecordType.CheckInProtectedReport

        return result

        # TODO: create object from protobuf & return

    class Meta:
        unique_together = ("package", "position")
