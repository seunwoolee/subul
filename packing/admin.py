from django.contrib import admin
from .models import PackingCode, Packing, AutoPacking


class PackingAdmin(admin.ModelAdmin):

    list_filter = ["id"]
    list_display = ["id", "type", "ymd", "codeName"]
    search_fields = ["id", "ymd", "codeName"]


class PackingCodeAdmin(admin.ModelAdmin):

    list_filter = ["code"]
    list_display = ["code", "codeName", "delete_state", "type"]
    search_fields = ["code", "codeName"]


class AutoPackingAdmin(admin.ModelAdmin):

    search_fields = ["productCode__codeName", "packingCode__codeName"]


admin.site.register(Packing, PackingAdmin)
admin.site.register(PackingCode, PackingCodeAdmin)
admin.site.register(AutoPacking, AutoPackingAdmin)