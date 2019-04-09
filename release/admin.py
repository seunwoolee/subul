from django.contrib import admin
from core.admin import DumbPaginator
from .models import Release


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = ["id", "ymd", "codeName", "releaseLocationName", "releaseOrder"]
    search_fields = ["id"]
    raw_id_fields = ("product_id", "releaseOrder")
    paginator = DumbPaginator
