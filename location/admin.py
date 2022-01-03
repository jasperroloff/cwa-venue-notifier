from typing import Union

from django.contrib import admin

# Register your models here.
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.utils.formats import localize

from location.models import Location
from warning.models import TraceTimeIntervalWarning, CheckInProtectedReport


class PackageContentInline(admin.StackedInline):
    fields = (
        ('package', 'position'),
        'check_in_record_start', 'check_in_record_duration', 'check_in_record_transmission_risk_level',
    )
    readonly_fields = (
        'package', 'position',
        'check_in_record_start', 'check_in_record_duration', 'check_in_record_transmission_risk_level',
    )
    can_delete = False
    show_full_result_count = True
    show_change_link = True

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @admin.display
    def package(self, obj: Union[TraceTimeIntervalWarning, CheckInProtectedReport]):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:warning_tracewarningpackage_change", args=(obj.package.pk,)),
            obj.location
        ))

    @admin.display(description=_("Start"))
    def check_in_record_start(self, obj: Union[TraceTimeIntervalWarning, CheckInProtectedReport]):
        return localize(obj.check_in_record.start)

    @admin.display(description=_("Duration"))
    def check_in_record_duration(self, obj: Union[TraceTimeIntervalWarning, CheckInProtectedReport]):
        return localize(obj.check_in_record.duration)

    @admin.display(description=_("Transmission Risk Level"))
    def check_in_record_transmission_risk_level(self, obj: Union[TraceTimeIntervalWarning, CheckInProtectedReport]):
        return obj.check_in_record.transmission_risk_level


class TraceTimeIntervalWarningInline(PackageContentInline):
    model = TraceTimeIntervalWarning


class CheckInProtectedReportInline(PackageContentInline):
    model = CheckInProtectedReport


class LocationAdmin(admin.ModelAdmin):
    fields = ('description', 'address', 'provider', 'url', 'uuid')
    readonly_fields = ('description', 'address', 'provider', 'url', 'uuid')
    list_display = ('description', 'provider')

    inlines = [
        CheckInProtectedReportInline,
        TraceTimeIntervalWarningInline,
    ]

    def get_fields(self, request, obj=None):
        if not obj:
            return ('url',)
        return super(LocationAdmin, self).get_fields(request, obj)

    def get_readonly_fields(self, request, obj=None):
        ret = list(super(LocationAdmin, self).get_readonly_fields(request, obj))
        if not obj:
            ret.remove('url')
        return tuple(ret)


admin.site.register(Location, LocationAdmin)
