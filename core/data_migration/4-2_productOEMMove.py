import os

import cx_Oracle

# cx_Oracle 한글처리 시작
from core.models import Location
from product.models import ProductCode, ProductMaster, ProductEgg, Product, ProductAdmin
from release.models import Release

os.environ["NLS_LANG"] = ".AL32UTF8"
START_VALUE = u"Unicode \u3042 3".encode('utf-8')
END_VALUE = u"Unicode \u3042 6".encode('utf-8')
# cx_Oracle 한글처리 끝

con = cx_Oracle.connect('system/kcerp@112.216.66.219/kcerp')
cursor = con.cursor()
# 고유 생성만 실시
query = " select * from kcfeed.FRESH상품 where 구분1 = 1 and 수량 > 0"
cursor.execute(query)
for i, row in enumerate(cursor, start=95000):
    id = i
    productYmd = row[2]
    to_location = row[5]
    productCode = row[6]
    productCodeName = row[7]
    count = row[8]
    amount = row[8]
    ymd = row[18]
    from_location = row[19]

    product = Product.objects.filter(ymd=productYmd).filter(code=productCode).first()
    product_Instance = ProductCode.objects.get(code=productCode)

    toLocation_instance = Location.objects.get(code=to_location)
    fromLocation_instance = Location.objects.get(code=from_location)
    # if not from_location:
    #     fromLocation_instance = Location.objects.get(code='00301')
    # else:
    #     fromLocation_instance = Location.objects.get(code=from_location)

    release = Release.objects.create(
        id=id,
        ymd=ymd,
        code=productCode,
        codeName=productCodeName,
        count=count,
        amount=amount,
        amount_kg=product_Instance.amount_kg,
        type='이동',
        product_id=product,
        productYmd=productYmd,
        releaseLocationCode=toLocation_instance,
        releaseLocationName=toLocation_instance.codeName,
        price=0,
        releaseVat=0,
        releaseStoreLocation=fromLocation_instance
    )

    ProductAdmin.objects.create(
        product_id=product,
        amount=-amount,
        count=-count,
        ymd=ymd,
        location=fromLocation_instance,
        releaseType='이동',
        releaseSeq=release
    )

    ProductAdmin.objects.create(
        product_id=product,
        amount=amount,
        count=count,
        ymd=ymd,
        location=toLocation_instance,
        releaseType='생성',
        releaseSeq=release
    )

print('productOEMMove 완료')
