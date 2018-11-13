from django.contrib import admin
from .models import Release


myModels = [Release]

admin.site.register(myModels)
# Register your models here.
