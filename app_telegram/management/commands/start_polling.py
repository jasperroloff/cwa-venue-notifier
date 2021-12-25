from django.core.management.base import BaseCommand

import app_telegram.telegram


class Command(BaseCommand):
    help = 'Run the telegram bot'

    def handle(self, *args, **options):
        app_telegram.telegram.run()
