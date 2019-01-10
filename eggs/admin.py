from django.contrib import admin
from .models import Egg, EggCode

myModels = [Egg, EggCode]

admin.site.register(myModels)