import re
import os.path
from typing import List

from click import group
from django.core.files.storage import default_storage, Storage
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

from warning.models import TraceWarningPackage
from warning.tasks import process_package, download_packages, import_packages


class Command(BaseCommand):
    help = 'Import warnings from CDN or filesystem'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-download',
            default=False,
            action='store_true',
            # help='Delete poll instead of closing it',
        )

        parser.add_argument(
            '--from-fs',
            default=False,
            action='store_true',
            # help='Delete poll instead of closing it',
        )

        parser.add_argument(
            '--overwrite',
            default=False,
            action='store_true',
            # help='Delete poll instead of closing it',
        )

    def handle(self, *args, **options):
        # ensure directory exists
        os.makedirs(settings.PACKAGES_DIR, exist_ok=True)

        if options['from_fs']:
            self.stdout.write(self.style.NOTICE('Importing ...'))
            count = import_packages.s(force=options['overwrite'])()
            self.stdout.write(self.style.SUCCESS('Successfully imported %d packages' % count))

        if not options['skip_download']:
            self.stdout.write(self.style.NOTICE('Downloading ...'))
            count = download_packages.s(force=options['overwrite'])()
            self.stdout.write(self.style.SUCCESS('Successfully downloaded %d packages' % count))
