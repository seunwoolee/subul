from django.contrib import admin
from .models import ReleaseMaster, Release


myModels = [Release,ReleaseMaster]

admin.site.register(myModels)
# Register your models here.
