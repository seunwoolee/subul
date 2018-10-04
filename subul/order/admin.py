from django.contrib import admin
from .models import Order, OrderMaster

myModels = [Order,OrderMaster]

admin.site.register(myModels)