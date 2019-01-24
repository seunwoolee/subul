from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):

    list_filter = ["id"]
    list_display = ["id", "ymd", "codeName", "orderLocationName", "release_id"]
    search_fields = ["id", "ymd", "codeName", "orderLocationName"]
    exclude = ["release_id"]


admin.site.register(Order, OrderAdmin)