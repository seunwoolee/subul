import os

import cx_Oracle

# cx_Oracle 한글처리 시작
from core.models import Location
from product.models import ProductCode, ProductMaster, ProductEgg, Product, ProductAdmin

os.environ["NLS_LANG"] = ".AL32UTF8"
START_VALUE = u"Unicode \u3042 3".encode('utf-8')
END_VALUE = u"Unicode \u3042 6".encode('utf-8')
# cx_Oracle 한글처리 끝

con = cx_Oracle.connect('system/kcerp@155.1.19.2/kcerp')
cursor = con.cursor()
# 고유 생성만 실시
query = " select '' 문서번호,'' 일련번호,생산일,제품코드,제품명,\
               조정구분,'' 구분,재살균일,sum(충진량) as 생산량, min(기타) as 기타,\
               sum(nvl(rawtank,0)) rawtank,sum(nvl(pasttank,0)) pasttank,\
               sum(nvl(loss0,0)) loss0,\
               sum(nvl(loss1,0)) loss1,\
               sum(nvl(loss2,0) + nvl(loss3,0) + nvl(loss4,0)) loss4,\
               sum(nvl(loss5,0) + nvl(loss6,0) + nvl(loss7,0)) loss7,\
               '' 현위치,'' 전위치,'' 이동일 \
        from   kcfeed.fresh제품생산d \
        where  조정구분 in ('할란' , '할란사용' ,'공정품투입' , '공정품발생' ,'제품생산')\
        group  by 생산일,제품코드,제품명,조정구분,재살균일\
        order  by 생산일 desc,문서번호,일련번호   "
cursor.execute(query)
master_instance = None
# diffYmd = 0
for row in cursor:
    # LOSS1 :할란, LOSS4 :살균 , LOSS7 : 충진불량 , LOSS0 : 투입
    # LOSS 1+2 , LOSS3+4 , LOSS 5+7, LOSS6+0
    # master_id = row[0]
    ymd = row[2]
    # diffYmd = ymd
    productCode = row[3]
    productCodeName = row[4]
    type = row[5]
    amount = row[8]
    memo = row[9]
    rawTank_amount = row[10]
    pastTank_amount = row[11]
    loss_insert = row[12]
    loss_openEgg = row[13]
    loss_clean = row[14]
    loss_fill = row[15]
    product_Instance = ProductCode.objects.get(code=productCode)
    count = round(amount / product_Instance.amount_kg)

    master_instance = ProductMaster.objects.filter(ymd=ymd).first()
    if not master_instance:
        master_instance = ProductMaster.objects.create(
            ymd=ymd
        )
    # master_instance = ProductMaster.objects.filter(id=master_id).first()
    # if not master_instance:

    if type == '제품생산':
        product = Product.objects.create(
            master_id=master_instance,
            ymd=ymd,
            code=productCode,
            codeName=productCodeName,
            amount=amount,
            count=count,
            amount_kg=product_Instance.amount_kg,
            memo=memo,
            loss_fill=loss_fill,
            loss_clean=loss_clean,
            productCode=product_Instance
        )
        ProductAdmin.objects.create(
            product_id=product,
            amount=amount,
            count=count,
            ymd=ymd,
            location=Location.objects.get(code='00301')
        )
    else:
        ProductEgg.objects.create(
            master_id=master_instance,
            ymd=ymd,
            type=type,
            code=productCode,
            codeName=productCodeName,
            rawTank_amount=rawTank_amount,
            pastTank_amount=pastTank_amount,
            loss_insert=loss_insert,
            loss_openEgg=loss_openEgg,
            memo=memo
        )

print('productEgg 완료')