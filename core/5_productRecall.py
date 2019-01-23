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
        where  생산일 < '20180521' and 조정구분 like '%미출고%' and 재살균일 >= '20181017'\
        union\
        select 문서번호,일련번호,생산일,제품코드,제품명,\
               조정구분, 구분,재살균일,충진량 as 생산량,기타,\
               nvl(rawtank,0) rawtank,nvl(pasttank,0) pasttank,nvl(loss0,0) loss0,nvl(loss1,0) loss1,nvl(loss4,0) loss4,nvl(loss7,0) loss7,현위치,전위치,이동일\
        from   kcfeed.fresh제품생산d\
        where  생산일 >= '20180521' and 조정구분 like '%미출고%' and 재살균일 >= '20181017'\
        order  by 생산일 ,문서번호,일련번호"
cursor.execute(query)
for i, row in enumerate(cursor):
    productYmd = row[2]
    productCode = row[3]
    ymd = row[7]
    amount = row[8]
    product = Product.objects.filter(ymd=productYmd).filter(code=productCode).first()
    product_Instance = ProductCode.objects.get(code=productCode)
    count = round(Decimal(amount) / product_Instance.amount_kg)
    location=Location.objects.get(code='00301')
    Product.objects.create(
        ymd=product.ymd,
        code=product.code,
        codeName=product.codeName,
        type="미출고품사용",
        amount=amount,
        count=count,
        amount_kg=product.amount_kg,
        master_id=product.master_id,
        productCode=product.productCode
    )
    ProductAdmin.objects.create(
        product_id=product,
        amount=amount,
        count=count,
        ymd=ymd,
        location=location,
        releaseType='미출고품사용'
    )

    CODE_TYPE_CHOICES = {
        '01201': 'RAW Tank 전란',
        '01202': 'RAW Tank 난황',
        '01203': 'RAW Tank 난백',
    }
    if product.productCode.type == "전란":
        egg_code = '01201'
        egg_codeName = CODE_TYPE_CHOICES['01201']
    elif product.productCode.type == "난황":
        egg_code = '01202'
        egg_codeName = CODE_TYPE_CHOICES['01202']
    else:
        egg_code = '01203'
        egg_codeName = CODE_TYPE_CHOICES['01203']

    ProductEgg.objects.create(
        code=egg_code,
        codeName=egg_codeName,
        ymd=ymd,
        type='미출고품사용',
        rawTank_amount=-amount,
        master_id=product.master_id,
    )

    ProductEgg.objects.create(
        code=egg_code,
        codeName=egg_codeName,
        ymd=ymd,
        type='미출고품투입',
        rawTank_amount=amount,
        master_id=product.master_id,
    )

print('productRecall 완료')
