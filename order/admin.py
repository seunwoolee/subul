from django.contrib import admin

from core.admin import DumbPaginator
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "ymd", "codeName", "orderLocationName", "release_id"]
    search_fields = ["id", "ymd", "codeName", "orderLocationName"]
    raw_id_fields = ("release_id", "productCode", "setProduct", "orderLocationCode")
    paginator = DumbPaginator
