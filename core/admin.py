from django.contrib import admin
from .models import Location, Audit, OrderTime
from django.core.paginator import Paginator
from django.utils.functional import cached_property


class DumbPaginator(Paginator):
    """
   Paginator that does not count the rows in the table.
   """
    @cached_property
    def count(self):
        return 999999


class LocationAdmin(admin.ModelAdmin):
    list_filter = ["code"]
    list_display = ["code", "codeName", "delete_state", "type", 'location_shoppingmall', 'location_character',
                    'location_manager']
    search_fields = ["code", "codeName", 'type']


admin.site.register(Location, LocationAdmin)
admin.site.register(Audit)
admin.site.register(OrderTime)
# Register your models here.
