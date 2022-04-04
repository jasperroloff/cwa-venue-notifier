import datetime
import hashlib
import hmac
import os
from typing import Union
from zoneinfo import ZoneInfo

from django.conf import settings
from django.db import models

from django.utils.translation import gettext as _

from Crypto.Cipher import AES

from location.models import Location
from proto import trace_warning_pb2


class CustomForeignKey(models.ForeignKey):
    __attname: str

    def __init__(self, *args, **kwargs):
        self.__attname = kwargs.pop("attname", None)
        super(CustomForeignKey, self).__init__(*args, **kwargs)

    def get_attname(self):
        return self.__attname or super(CustomForeignKey, self).get_attname()


class TraceWarningPackage(models.Model):
    api_version = models.IntegerField(
        editable=False,
        verbose_name=_("API Version"),
        help_text=_("Version of the API"),
    )
    interval_number = models.BigIntegerField(
        editable=False,
        verbose_name=_("Interval Number"),
        help_text=_("Interval in hours since UNIX epoch"),
    )
    region = models.CharField(
        editable=False,
        max_length=2,
        verbose_name=_("Region"),
        help_text=_("For example 'DE'"),
    )

    imported_at = models.DateTimeField(
        null=True,
        verbose_name=_("Imported at"),
    )

    @property
    def filename(self) -> str:
        return f"{self.interval_number}_{self.region}_v{self.api_version}.zip"

    @property
    def filepath(self):
        return os.path.join(settings.PACKAGES_DIR, self.filename)

    @property
    def name(self):
        return f"{self.region}/v{self.api_version}/{self.interval_number}"

    @property
    def interval(self):
        return (datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
                + datetime.timedelta(hours=self.interval_number)).astimezone(tz=ZoneInfo(settings.TIME_ZONE))

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("api_version", "interval_number", "region")
        ordering = ['-interval_number', 'region', '-api_version']


class CheckInRecordType:
    TraceTimeIntervalWarning = "TraceTimeIntervalWarning"
    CheckInProtectedReport = "CheckInProtectedReport"

    choices = (
        (TraceTimeIntervalWarning, "TraceTimeIntervalWarning"),
        (CheckInProtectedReport, "CheckInProtectedReport"),
    )


class CheckInRecord(models.Model):
    start_interval_number = models.BigIntegerField(
        editable=False,
        verbose_name=_("Start interval number"),
        help_text=_("Start interval in 10 minute steps since UNIX epoch"),
    )
    period = models.BigIntegerField(
        editable=False,
        verbose_name=_("Period"),
        help_text=_("Warning duration in 10 minute steps"),
    )
    transmission_risk_level = models.IntegerField(
        editable=False,
        verbose_name=_("Transmission Risk Level"),
        # help_text=_(""),
    )
    type = models.CharField(
        editable=False,
        choices=CheckInRecordType.choices,
        max_length=30,
    )

    @property
    def start(self) -> datetime.datetime:
        return (datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
                + datetime.timedelta(minutes=self.start_interval_number * 10))\
            .astimezone(tz=ZoneInfo(settings.TIME_ZONE))

    @property
    def end(self) -> datetime.datetime:
        return self.start + self.duration

    @property
    def duration(self) -> datetime.timedelta:
        return datetime.timedelta(minutes=10 * self.period)

    class Meta:
        managed = False

    def __eq__(self, other: "CheckInRecord"):
        return self.start_interval_number == other.start_interval_number and self.period == other.period and self.transmission_risk_level == other.transmission_risk_level

    def __hash__(self):
        return hash(('start_interval_number', self.start_interval_number, 'period', self.period, 'transmission_risk_level', self.transmission_risk_level))


class TraceTimeIntervalWarning(models.Model):
    package = models.ForeignKey(
        TraceWarningPackage,
        on_delete=models.CASCADE,
        editable=False,
        verbose_name=_("Package"),
        help_text=_("The warning package, where this time interval warning comes from"),
    )
    position = models.IntegerField(
        editable=False,
        # verbose_name=_("Location ID Hash"),
        # help_text=_("SHA256 hash of the location ID"),
    )
    location = CustomForeignKey(
        Location,
        on_delete=models.DO_NOTHING,
        to_field="location_id_hash",
        db_column="location_id_hash",
        db_constraint=False,
        attname='location_id_hash',
        editable=False,
    )
    location_id_hash: memoryview
    #location_id_hash = models.BinaryField(
    #    verbose_name=_("Location ID Hash"),
    #    help_text=_("SHA256 hash of the location ID"),
    #    db_column="location_id_hash",
    #)

    start_interval_number = models.BigIntegerField(
        editable=False,
        verbose_name=_("Start interval number"),
        help_text=_("Start interval in 10 minute steps since UNIX epoch"),
    )
    period = models.BigIntegerField(
        editable=False,
        verbose_name=_("Period"),
        help_text=_("Warning duration in 10 minute steps"),
    )
    transmission_risk_level = models.BigIntegerField(
        editable=False,
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

    @property
    def name(self):
        return f"TraceTimeIntervalWarning  {self.package}#{self.position}"

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("package", "position")
        ordering = ['-package', '-position']


class CheckInProtectedReport(models.Model):
    package = models.ForeignKey(
        TraceWarningPackage,
        on_delete=models.CASCADE,
        editable=False,
        verbose_name=_("Package"),
        help_text=_("The warning package, where this protected check-in report comes from"),
    )
    position = models.IntegerField(
        editable=False,
        # verbose_name=_("Location ID Hash"),
        # help_text=_("SHA256 hash of the location ID"),
    )
    location = CustomForeignKey(
        Location,
        on_delete=models.DO_NOTHING,
        to_field="location_id_hash",
        db_column="location_id_hash",
        db_constraint=False,
        attname='location_id_hash',
        editable=False,
    )
    location_id_hash: memoryview
    # location_id_hash = models.BinaryField(
    #    verbose_name=_("Location ID Hash"),
    #    help_text=_("SHA256 hash of the location ID"),
    #    db_column="location_id_hash",
    # )
    iv: bytes = models.BinaryField(
        editable=False,
        verbose_name=_("IV"),
        # help_text=_(""),
    )
    encrypted_check_in_record: bytes = models.BinaryField(
        editable=False,
        verbose_name=_("Encrypted Check-In Record"),
        # help_text=_(""),
    )
    mac: bytes = models.BinaryField(
        editable=False,
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

    @property
    def name(self):
        return f"CheckInProtectedReport {self.package}#{self.position}"

    @property
    def check_in_record(self) -> Union[CheckInRecord, None]:
        try:
            return self.decrypt(self.location.location_id)
        except:
            return None

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("package", "position")
        ordering = ['-package', '-position']
