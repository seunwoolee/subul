from django.contrib import admin
from .models import Order

myModels = [Order]

admin.site.register(myModels)