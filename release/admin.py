from django.contrib import admin
from .models import Release


class ReleaseAdmin(admin.ModelAdmin):

    list_filter = ["id"]
    list_display = ["id", "ymd", "codeName", "releaseLocationName", "releaseOrder"]
    search_fields = ["id", "ymd", "codeName", "releaseLocationName"]
    exclude = ["releaseOrder"]


admin.site.register(Release, ReleaseAdmin)