from django.contrib import admin

# Register your models here.
from location.models import Location


class LocationAdmin(admin.ModelAdmin):
    fields = ('description', 'address', 'provider', 'url')
    readonly_fields = ('description', 'address', 'provider', 'url')
    list_display = ('description', 'provider')

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
