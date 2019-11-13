from django.contrib import admin
from core.admin import DumbPaginator
from .models import Release, Car


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = ["id", "ymd", "codeName", "releaseLocationName", "releaseOrder"]
    search_fields = ["id"]
    raw_id_fields = ("product_id", "releaseOrder")
    paginator = DumbPaginator


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ["id", "car_number", "type", "palette_count"]
    search_fields = ["car_number"]
