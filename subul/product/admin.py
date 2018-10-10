from django.contrib import admin
from .models import Product, ProductAdmin, ProductCode, ProductMaster, ProductEgg, ProductUnitPrice, SetProductCode\
    , SetProductMatch


myModels = [Product,
            ProductAdmin,
            ProductCode,
            ProductMaster,
            ProductEgg,
            ProductUnitPrice,
            SetProductCode,
            SetProductMatch]

admin.site.register(myModels)