from django.contrib import admin
from .models import PackingCode, Packing

myModels = [PackingCode, Packing]

admin.site.register(myModels)