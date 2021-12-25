from django.contrib import admin

# Register your models here.
from app_telegram.models import WarningSubscription

admin.site.register(WarningSubscription)
