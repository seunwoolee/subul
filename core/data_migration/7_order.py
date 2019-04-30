import os

import cx_Oracle
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "subul.settings")
django.setup()

# cx_Oracle 한글처리 시작
from core.models import Location
from order.models import Order
from product.models import ProductCode, ProductMaster, ProductEgg, Product, ProductAdmin, SetProductCode
from release.models import Release

os.environ["NLS_LANG"] = ".AL32UTF8"
START_VALUE = u"Unicode \u3042 3".encode('utf-8')
END_VALUE = u"Unicode \u3042 6".encode('utf-8')
# cx_Oracle 한글처리 끝

con = cx_Oracle.connect('system/kcerp@155.1.19.2/kcerp')
cursor = con.cursor()
# 고유 생성만 실시
query = " select * from kcfeed.fresh주문 "
cursor.execute(query)
for i, row in enumerate(cursor):
    id = row[0]
    ymd = row[1]
    locationCode = row[3]
    locationCodeName = row[4]
    productCode = row[5]
    count = row[6]
    amount = row[7]
    memo = row[8]
    type = row[9]
    price = row[15]
    setProductCode = row[17]
    product_Instance = ProductCode.objects.get(code=productCode)
    toLocation_instance = Location.objects.get(code=locationCode)

    if not count:
        count = 0

    if not price:
        price = 0

    if not type:
        type = '판매'
    try:
        order = Order.objects.create(
            id=id,
            ymd=ymd,
            code=productCode,
            codeName=product_Instance.codeName,
            count=count,
            amount=amount,
            amount_kg=product_Instance.amount_kg,
            memo=memo,
            productCode=product_Instance,
            orderLocationCode=toLocation_instance,
            orderLocationName=locationCodeName,
            type=type,
            price=price
        )

        if setProductCode:
            order.setProduct = SetProductCode.objects.get(code=setProductCode)
        order.save()
    except:
        print(id)
print('order 완료')
