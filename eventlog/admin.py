from django.contrib import admin

from core.admin import DumbPaginator
from .models import Log


class LogAdmin(admin.ModelAdmin):

    raw_id_fields = ["user"]
    list_display = ["timestamp", "user", "action", "extra"]
    search_fields = ["user__username", "action", "extra"]
    paginator = DumbPaginator


admin.site.register(Log, LogAdmin)