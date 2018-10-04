from django.contrib import admin
from .models import *


myModels = [Order,OrderMaster]

admin.site.register(myModels)
# Register your models here.
