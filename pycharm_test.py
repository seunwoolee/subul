import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = "subul.settings"
django.setup()

from product.models import Product
print(Product.objects.last())
