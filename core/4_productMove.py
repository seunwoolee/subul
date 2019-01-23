import os
from decimal import Decimal
import cx_Oracle

# cx_Oracle 한글처리 시작
from core.models import Location
from product.models import ProductCode, ProductMaster, ProductEgg, Product, ProductAdmin
from release.models import Release

os.environ["NLS_LANG"] = ".AL32UTF8"
START_VALUE = u"Unicode \u3042 3".encode('utf-8')
END_VALUE = u"Unicode \u3042 6".encode('utf-8')
# cx_Oracle 한글처리 끝

con = cx_Oracle.connect('system/kcerp@155.1.19.2/kcerp')
cursor = con.cursor()
# 고유 생성만 실시
query = " select 문서번호,일련번호,생산일,제품코드,제품명,\
       조정구분, 구분,재살균일,충진량 as 생산량,기타,\
       nvl(rawtank,0) rawtank,nvl(pasttank,0) pasttank,nvl(loss0,0) loss0,nvl(loss1,0) loss1,nvl(loss2,0) + nvl(loss3,0) + nvl(loss4,0) loss4,nvl(loss5,0) + nvl(loss6,0) + nvl(loss7,0) loss7,현위치,전위치,이동일\
        from   kcfeed.fresh제품생산d\
        where  생산일 < '20180521'and 조정구분 = '이동' and 충진량 > 0 \
        union\
        select 문서번호,일련번호,생산일,제품코드,제품명,\
               조정구분, 구분,재살균일,충진량 as 생산량,기타,\
               nvl(rawtank,0) rawtank,nvl(pasttank,0) pasttank,nvl(loss0,0) loss0,nvl(loss1,0) loss1,nvl(loss4,0) loss4,nvl(loss7,0) loss7,현위치,전위치,이동일\
        from   kcfeed.fresh제품생산d\
        where  생산일 >= '20180521' and 조정구분 = '이동'  and 충진량 > 0\
        order  by 생산일 ,문서번호,일련번호"
cursor.execute(query)
for i, row in enumerate(cursor, start=85000):
    id = i
    print(id)
    productYmd = row[2]
    productCode = row[3]
    productCodeName = row[4]
    amount = row[8]
    to_location = row[16]
    from_location = row[17]
    ymd = row[18]
    product = Product.objects.filter(ymd=productYmd).filter(code=productCode).first()
    product_Instance = ProductCode.objects.get(code=productCode)
    count = round(Decimal(amount) / product_Instance.amount_kg)

    toLocation_instance = Location.objects.get(code=to_location)
    if not from_location:
        fromLocation_instance = Location.objects.get(code='00301')
    else:
        fromLocation_instance = Location.objects.get(code=from_location)

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

print('productMove 완료')
