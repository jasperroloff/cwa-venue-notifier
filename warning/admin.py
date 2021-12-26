from typing import Union

from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from django.utils.formats import localize


# Register your models here.
from location.models import Location
from warning.models import TraceWarningPackage, TraceTimeIntervalWarning, CheckInProtectedReport


class PackageContentInline(admin.TabularInline):
    fields = ('position', 'location')
    readonly_fields = ('position', 'location')
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
    def location(self, obj: Union[TraceTimeIntervalWarning, CheckInProtectedReport]):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:location_location_change", args=(obj.location.pk,)),
            obj.location
        ))


class TraceTimeIntervalWarningInline(PackageContentInline):
    model = TraceTimeIntervalWarning


class CheckInProtectedReportInline(PackageContentInline):
    model = CheckInProtectedReport


class TraceWarningPackageAdmin(admin.ModelAdmin):
    fields = ('api_version', 'region', ('interval_number', 'interval'), 'imported_at')
    readonly_fields = ('api_version', 'region', 'interval_number', 'interval', 'imported_at')
    list_display = ('name', 'interval', 'imported_at')
    date_hierarchy = 'imported_at'
    search_fields = ('interval_number',)
    inlines = [
        TraceTimeIntervalWarningInline,
        CheckInProtectedReportInline,
    ]

    @admin.display(description=_('Interval datetime'))
    def interval(self, obj: TraceWarningPackage):
        return localize(obj.interval, use_l10n=True)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class PackageContentAdmin(admin.ModelAdmin):
    readonly_fields = (
        'location', 'check_in_record_start', 'check_in_record_duration', 'check_in_record_transmission_risk_level',
    )

    @admin.display(description=_("Location"))
    def location(self, obj: Union[TraceTimeIntervalWarning, CheckInProtectedReport]):
        try:
            return mark_safe('<a href="{}">{}</a>'.format(
                reverse("admin:location_location_change", args=(obj.location.pk,)),
                obj.location
            ))
        except Location.DoesNotExist:
            return None

    @admin.display(description=_("Start"))
    def check_in_record_start(self, obj: Union[TraceTimeIntervalWarning, CheckInProtectedReport]):
        return localize(obj.check_in_record.start)

    @admin.display(description=_("Duration"))
    def check_in_record_duration(self, obj: Union[TraceTimeIntervalWarning, CheckInProtectedReport]):
        return localize(obj.check_in_record.duration)

    @admin.display(description=_("Transmission Risk Level"))
    def check_in_record_transmission_risk_level(self, obj: Union[TraceTimeIntervalWarning, CheckInProtectedReport]):
        return obj.check_in_record.transmission_risk_level

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(TraceWarningPackage, TraceWarningPackageAdmin)
admin.site.register(TraceTimeIntervalWarning, PackageContentAdmin)
admin.site.register(CheckInProtectedReport, PackageContentAdmin)
