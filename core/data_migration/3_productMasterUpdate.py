import os

import cx_Oracle

# cx_Oracle 한글처리 시작
from django.db.models import Sum

from core.models import Location
from product.models import ProductCode, ProductMaster, ProductEgg, Product, ProductAdmin

for ele in ProductEgg.objects.values('master_id').annotate(Sum('loss_insert')).annotate(Sum('loss_openEgg')):
    productMaster = ProductMaster.objects.get(id=ele['master_id'])
    productMaster.total_loss_insert = ele['loss_insert__sum']
    productMaster.total_loss_openEgg = ele['loss_openEgg__sum']
    productMaster.save()

for ele in Product.objects.values('master_id').annotate(Sum('loss_clean')).annotate(Sum('loss_fill')):
    productMaster = ProductMaster.objects.get(id=ele['master_id'])
    productMaster.total_loss_clean = ele['loss_clean__sum']
    productMaster.total_loss_fill = ele['loss_fill__sum']
    productMaster.save()

print('ProductMaster TOTAL LOSS Update 완료')