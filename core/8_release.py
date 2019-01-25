import os
from decimal import Decimal

import cx_Oracle

# cx_Oracle 한글처리 시작
from core.models import Location
from order.models import Order
from product.models import ProductCode, ProductMaster, ProductEgg, Product, ProductAdmin, SetProductCode
from release.models import Release

os.environ["NLS_LANG"] = ".AL32UTF8"
START_VALUE = u"Unicode \u3042 3".encode('utf-8')
END_VALUE = u"Unicode \u3042 6".encode('utf-8')
# cx_Oracle 한글처리 끝

con = cx_Oracle.connect('system/kcerp@112.216.66.219/kcerp')
cursor = con.cursor()
# 고유 생성만 실시
query = " select * from kcfeed.FRESH판매 order by '문서번호' "
cursor.execute(query)
for i, row in enumerate(cursor):
    id=row[0]
    ymd=row[1]
    locationCode = row[2]
    locationCodeName = row[3]
    productCode = row[4]
    productCodeName = row[5]
    amount = row[6]
    price = row[7]
    productYmd = row[15]
    type = row[16]
    order = row[17]
    storedLocation = row[19]
    setProductCode = row[20]
    releaseVat = row[21]

    print(row)
    product = Product.objects.filter(ymd=productYmd).filter(code=productCode).first()
    product_Instance = ProductCode.objects.get(code=productCode)
    toLocation_instance = Location.objects.filter(code=locationCode).first()
    fromLocation_instance = Location.objects.get(code=storedLocation)
    count = round(Decimal(amount) / product_Instance.amount_kg)

    if not price:
        price=0

    if not releaseVat:
        releaseVat=0

    if not type:
        if price > 0:
            type="판매"
        else:
            type="증정"

    if not toLocation_instance:
        toLocation_instance = fromLocation_instance

    release = Release.objects.create(
        id=id,
        ymd=ymd,
        code=productCode,
        codeName=productCodeName,
        count=count,
        amount=amount,
        amount_kg=product_Instance.amount_kg,
        type=type,
        product_id=product,
        productYmd=productYmd,
        releaseLocationCode=toLocation_instance,
        releaseLocationName=locationCodeName,
        price=price,
        releaseStoreLocation=fromLocation_instance,
        releaseVat=releaseVat
    )

    if order > 0:
        try:
            order_instance = Order.objects.get(id=order)
        except:
            order_instance = None

        if order_instance:
            release.releaseOrder = order_instance
            order_instance.release_id = release
            order_instance.save()

    if setProductCode:
        release.releaseSetProductCode=SetProductCode.objects.get(code=setProductCode)
    release.save()

    ProductAdmin.objects.create(
        product_id=product,
        count=-int(count),
        amount=-float(amount),
        ymd=ymd,
        location=fromLocation_instance,
        releaseType=type,
        releaseSeq=release
    )
print('release 완료')
