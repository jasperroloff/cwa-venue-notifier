import io
import logging
import os
import re
import zipfile
from typing import Union, List

import requests
from celery import shared_task, group
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.files.storage import default_storage

import app_telegram.telegram
from location.models import Location
from proto import trace_warning_pb2
from warning.models import TraceWarningPackage, CheckInProtectedReport, TraceTimeIntervalWarning, CheckInRecord


def send_warning(item: Union[CheckInProtectedReport, TraceTimeIntervalWarning], package: TraceWarningPackage):
    bot = app_telegram.telegram.get_bot()

    try:
        location = Location.objects.get(location_id_hash=item.location_id_hash)

        record: CheckInRecord
        if isinstance(item, CheckInProtectedReport):
            record = item.decrypt(location.location_id)
        elif isinstance(item, TraceTimeIntervalWarning):
            record = item.check_in_record
        else:
            return

        location_name = location.to_object().locationData.description

        for subscription in location.warningsubscription_set.all():
            logging.warning(f"Warning for Chat {subscription.chat} / Location {location_name}")

            bot.send_message(
                subscription.chat,
                text=render_to_string("telegram/check_in_record.html", {
                    'record': record,
                    'location': location_name,
                    'package': package,
                }),
                parse_mode="HTML",
            )
    except Location.DoesNotExist:
        pass


def process_time_interval_warning(item_bytes: bytes, package: TraceWarningPackage, index: int):
    item: trace_warning_pb2.TraceTimeIntervalWarning = trace_warning_pb2.TraceTimeIntervalWarning.FromString(item_bytes)

    obj, created = TraceTimeIntervalWarning.objects.update_or_create(
        package=package,
        position=index,
        location_id_hash=item.locationIdHash,
        start_interval_number=item.startIntervalNumber,
        period=item.period,
        transmission_risk_level=item.transmissionRiskLevel,
    )

    if created:
        send_warning(obj, package)


def process_check_in_protected_report(item_bytes: bytes, package: TraceWarningPackage, index: int):
    item = trace_warning_pb2.CheckInProtectedReport.FromString(item_bytes)

    obj, created = CheckInProtectedReport.objects.update_or_create(
        package=package,
        position=index,
        location_id_hash=item.locationIdHash,
        iv=item.iv,
        mac=item.mac,
        encrypted_check_in_record=item.encryptedCheckInRecord,
    )

    if created:
        send_warning(obj, package)


def process_package(zip_bytes: bytes, package: TraceWarningPackage):
    if len(zip_bytes) == 0:
        return

    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as package_zip:
        with package_zip.open("export.bin") as export_bin:
            package_bytes = export_bin.read()
            package_obj = trace_warning_pb2.TraceWarningPackage.FromString(package_bytes)

            for index, item in enumerate(package_obj.timeIntervalWarnings):
                item: trace_warning_pb2.TraceTimeIntervalWarning
                process_time_interval_warning(item.SerializeToString(), package, index)

            for index, item in enumerate(package_obj.checkInProtectedReports):
                item: trace_warning_pb2.CheckInProtectedReport
                process_check_in_protected_report(item.SerializeToString(), package, index)


@shared_task
def download_package(url: str, package: TraceWarningPackage):
    zip_bytes = requests.get(url).content
    with open(package.filepath, 'wb') as file:
        file.write(zip_bytes)
    process_package(zip_bytes, package)
    package.imported_at = timezone.now()
    package.save()


@shared_task
def import_package(package: TraceWarningPackage):
    with open(package.filepath, 'rb') as package_file:
        zip_bytes: bytes = package_file.read()
        process_package(zip_bytes, package)
        package.imported_at = timezone.now()
        package.save()


@shared_task
def download_packages(force: bool = False) -> int:
    count = 0
    tasks = []

    os.makedirs(settings.PACKAGES_DIR, exist_ok=True)

    for version in [1, 2]:
        version_url = f"{settings.CWA_BASE_URL}/version/v{version}"
        for region in settings.CWA_REGIONS:
            region_url = f"{version_url}/twp/country/{region}/hour"
            response = requests.get(region_url).json()
            for hour in range(response['oldest'], response['latest'] + 1):
                hour_url = f"{region_url}/{hour}"

                package, created = TraceWarningPackage.objects.get_or_create(
                    region=region,
                    api_version=version,
                    interval_number=hour,
                )

                if force or created or not os.path.exists(package.filepath):
                    tasks.append(download_package.s(hour_url, package))
                    count += 1

    group(tasks)()

    return count


@shared_task
def import_packages(force: bool) -> int:
    count = 0
    files: List[str] = default_storage.listdir(settings.PACKAGES_DIR)[1]
    tasks = []

    os.makedirs(settings.PACKAGES_DIR, exist_ok=True)

    for file in files:
        for hour, region, api_version in re.findall(r"(\d+)_([A-Z]+)_v(\d)\.zip$", file):
            package, created = TraceWarningPackage.objects.get_or_create(
                region=region,
                api_version=api_version,
                interval_number=hour,
            )

            if force or created:
                tasks.append(import_package.s(package))
                count += 1

    group(tasks)()

    return count
