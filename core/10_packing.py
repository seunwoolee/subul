import os
from decimal import Decimal

import cx_Oracle

# cx_Oracle 한글처리 시작
from core.models import Location
from eggs.models import EggCode, Egg
from order.models import Order
from packing.models import PackingCode, Packing
from product.models import ProductCode, ProductMaster, ProductEgg, Product, ProductAdmin, SetProductCode
from release.models import Release

os.environ["NLS_LANG"] = ".AL32UTF8"
START_VALUE = u"Unicode \u3042 3".encode('utf-8')
END_VALUE = u"Unicode \u3042 6".encode('utf-8')
# cx_Oracle 한글처리 끝
Egg.objects.all().delete()
con = cx_Oracle.connect('system/kcerp@155.1.19.2/kcerp')
cursor = con.cursor()
# 고유 생성만 실시
query = " select * from kcfeed.FRESH자재IO "
cursor.execute(query)

for i, row in enumerate(cursor):
    type=row[1]
    ymd=row[2]
    productCode = row[3]
    inLocationCode= row[4]
    outLocationCode = row[5]
    count = row[6]
    memo = row[7]
    price = row[12]

    if type == '1':
        type = '입고'
    elif type == '2':
        type = '생산'
        count = -count
    elif type == '4':
        type = '폐기'
        count = -count
    elif type == '3':
        type = '조정'

    print(outLocationCode)
    packing_instance = PackingCode.objects.filter(code=productCode).first()

    try:
        inLocation_instance = Location.objects.get(code=inLocationCode)
    except:
        inLocation_instance = None

    try:
        outLocation_instance = Location.objects.get(code=outLocationCode)
    except:
        outLocation_instance = None

    packing = Packing.objects.create(
        code=productCode,
        codeName=packing_instance.codeName,
        count=count,
        memo=memo,
        type=type,
        ymd=ymd,
        price=price,
        packingCode=packing_instance,
    )

    if inLocation_instance:
        packing.locationCode = inLocation_instance
        packing.locationCodeName = inLocation_instance.codeName
    packing.save()

print('Egg 완료')
