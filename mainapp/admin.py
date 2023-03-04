from django.contrib import admin
from mainapp.models import Street, Work, Address
from django.utils.translation import gettext_lazy as _


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ["pk", "name_street"]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["pk", "number_of_house", "get_street_name"]
    ordering = ["pk", "street__name_street", "number_of_house"]

    def get_street_name(self, obj):
        return obj.street.name_street

    get_street_name.short_description = _("Street")
