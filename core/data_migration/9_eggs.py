import os
from decimal import Decimal

import cx_Oracle

# cx_Oracle 한글처리 시작
from core.models import Location
from eggs.models import EggCode, Egg
from order.models import Order
from product.models import ProductCode, ProductMaster, ProductEgg, Product, ProductAdmin, SetProductCode
from release.models import Release

os.environ["NLS_LANG"] = ".AL32UTF8"
START_VALUE = u"Unicode \u3042 3".encode('utf-8')
END_VALUE = u"Unicode \u3042 6".encode('utf-8')
# cx_Oracle 한글처리 끝
Egg.objects.all().delete()
con = cx_Oracle.connect('system/kcerp@112.216.66.219/kcerp')
cursor = con.cursor()
# 고유 생성만 실시
query = " select 입고처,원란종류 계란종류,입고일,'0' 입출고구분,수량 From kcfeed.fresh원란마감 where  마감일 = '20131231'"
cursor.execute(query)
for row in cursor:
    inLocationCode = row[0]
    productCode = row[1]
    inYmd = row[2]
    type = '입고'
    count = row[4]

    egg_instance = EggCode.objects.filter(code=productCode).first()
    inLocation_instance = Location.objects.get(code=inLocationCode)
    Egg.objects.create(
            code=productCode,
            codeName=egg_instance.codeName,
            count=count,
            type=type,
            in_locationCode=inLocation_instance,
            in_locationCodeName=inLocation_instance.codeName,
            in_ymd=inYmd,
            ymd=inYmd,
            eggCode=egg_instance,
        )

query = " select 입고처,계란종류,입고일,입출고구분,수량 From kcfeed.fresh원란io Where  입고일 < '20140101' and 입고일 > '20131229' and    출고일 > '20131231' and 출고일 < '20140122' "
cursor.execute(query)
for row in cursor:
    inLocationCode = row[0]
    productCode = row[1]
    inYmd = row[2]
    type = row[3]
    count = row[4]

    if type == '1':
        type = '입고'
    elif type == '2':
        type = '생산'
        count = -count
    elif type == '4':
        type = '판매'
        count = -count
    elif type == '3':
        type = '폐기'
        count = -count

    egg_instance = EggCode.objects.filter(code=productCode).first()
    inLocation_instance = Location.objects.get(code=inLocationCode)
    Egg.objects.create(
            code=productCode,
            codeName=egg_instance.codeName,
            count=count,
            type=type,
            in_locationCode=inLocation_instance,
            in_locationCodeName=inLocation_instance.codeName,
            in_ymd=inYmd,
            ymd=inYmd,
            eggCode=egg_instance,
        )


query = " select * from kcfeed.fresh원란IO Where  입고일 >= '20140101'"
cursor.execute(query)

for i, row in enumerate(cursor):
    id=row[0]
    type=row[1]
    inYmd=row[2]
    productCode = row[3]
    outYmd= row[4]
    inLocationCode = row[5]
    count = row[6]
    memo = row[7]
    price = row[12]
    outLocationCode = row[13]
    amount = row[14]

    if type == '1':
        type = '입고'
    elif type == '2':
        type = '생산'
        count = -count
    elif type == '4':
        type = '판매'
        count = -count
    elif type == '3':
        type = '폐기'
        count = -count

    print(count)
    egg_instance = EggCode.objects.filter(code=productCode).first()
    inLocation_instance = Location.objects.get(code=inLocationCode)
    try:
        outLocation_instance = Location.objects.get(code=outLocationCode)
    except:
        outLocation_instance = None

    egg = Egg.objects.create(
        code=productCode,
        codeName=egg_instance.codeName,
        count=count,
        memo=memo,
        type=type,
        in_locationCode=inLocation_instance,
        in_locationCodeName=inLocation_instance.codeName,
        in_ymd=inYmd,
        ymd=inYmd,
        price=price,
        eggCode=egg_instance,
        amount=amount
    )

    if outLocation_instance:
        egg.ymd=outYmd
        egg.locationCode = outLocation_instance
        egg.locationCodeName = outLocation_instance.codeName

    if outYmd:
        egg.ymd=outYmd

    egg.save()

print('Egg 완료')
