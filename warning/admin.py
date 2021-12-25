from django.contrib import admin

# Register your models here.
from warning.models import TraceWarningPackage, TraceTimeIntervalWarning, CheckInProtectedReport

admin.site.register(TraceWarningPackage)
admin.site.register(TraceTimeIntervalWarning)
admin.site.register(CheckInProtectedReport)
