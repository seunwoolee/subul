from django.contrib import admin
from .models import Egg, EggCode, EggOrder, EggOrderMaster


@admin.register(Egg)
class EggAdmin(admin.ModelAdmin):

    list_filter = ["id"]
    list_display = ["id", "type", "ymd", "codeName"]
    search_fields = ["id", "ymd", "codeName"]


@admin.register(EggOrder)
class EggOrderAdmin(admin.ModelAdmin):

    list_filter = ["id"]
    list_display = ["id", "ymd", "in_locationCodeName", "codeName"]
    search_fields = ["id", "ymd", "codeName"]


admin.site.register(EggCode)
admin.site.register(EggOrderMaster)