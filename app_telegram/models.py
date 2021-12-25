from django.db import models

from location.models import Location


class WarningSubscription(models.Model):
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        verbose_name="Venue",
        #help_text="",
    )
    chat = models.BigIntegerField(
        verbose_name="Chat ID",
        help_text="Telegram chat",
    )

    class Meta:
        verbose_name = "Warning-Subscription"
        verbose_name_plural = "Warning-Subscriptions"
