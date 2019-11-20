from django.contrib import admin
from core.admin import DumbPaginator
from .models import Release, Car, Pallet, OrderList


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = ["id", "ymd", "codeName", "releaseLocationName", "releaseOrder"]
    search_fields = ["id"]
    raw_id_fields = ("product_id", "releaseOrder")
    paginator = DumbPaginator


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ["id", "car_number", "type"]
    search_fields = ["car_number"]


@admin.register(Pallet)
class PalletAdmin(admin.ModelAdmin):
    list_display = ["id", "car", "seq"]
    search_fields = ["car__car_number"]


@admin.register(OrderList)
class OrderListAdmin(admin.ModelAdmin):
    list_display = ["id", "location", "pallet"]
    search_fields = ["location__codeName", "pallet__car__car_number", "ymd"]
