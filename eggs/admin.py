from django.contrib import admin
from .models import Egg, EggCode


class EggAdmin(admin.ModelAdmin):

    list_filter = ["id"]
    list_display = ["id", "type", "ymd", "codeName"]
    search_fields = ["id", "ymd", "codeName"]


admin.site.register(Egg, EggAdmin)
admin.site.register(EggCode)