from django.contrib import admin
from .models import Location


class LocationAdmin(admin.ModelAdmin):
    list_filter = ["code"]
    list_display = ["code", "codeName", "delete_state", "type", 'location_shoppingmall', 'location_character',
                    'location_manager']
    search_fields = ["code", "codeName", 'type']


admin.site.register(Location, LocationAdmin)
# Register your models here.
