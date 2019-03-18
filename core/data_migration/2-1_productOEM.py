import os
from decimal import Decimal
import cx_Oracle

# cx_Oracle 한글처리 시작
from core.models import Location
from product.models import ProductCode, ProductMaster, ProductEgg, Product, ProductAdmin

os.environ["NLS_LANG"] = ".AL32UTF8"
START_VALUE = u"Unicode \u3042 3".encode('utf-8')
END_VALUE = u"Unicode \u3042 6".encode('utf-8')
# cx_Oracle 한글처리 끝

con = cx_Oracle.connect('system/kcerp@112.216.66.219/kcerp')
cursor = con.cursor()
# 고유 생성만 실시
query = " select '' 문서번호, MAX(구매일) as 구매일 , 생산일, MIN(거래처) as 거래처, MIN(거래처명) as 거래처명 , '00301' 현위치, \
         상품코드,상품명, sum(수량) as 수량, sum(금액) as 금액,sum(부가세) as 부가세, '' as 구분1, '' as 구분2 , '' as 입력자 , '' as 입력일 , '' as 수정자 , '' as 수정일 , MIN(메모)as 메모  \
         from kcfeed.FRESH상품 where 구분1 = 0 group by 생산일,상품코드,상품명"
cursor.execute(query)
master_instance= None
for row in cursor:
    purchaseYmd = row[1]
    ymd = row[2]
    purchaseLocation = row[3]
    purchaseLocationName = row[4]
    productCode = row[6]
    productCodeName = row[7]
    count = row[8]
    amount = row[8]
    purchaseSupplyPrice = row[9]
    purchaseVat = row[10]
    memo = row[17]

    product_Instance = ProductCode.objects.get(code=productCode)
    if not master_instance:
        master_instance = ProductMaster.objects.create(ymd='00000000')
    purchaseLocation = Location.objects.get(code=purchaseLocation)

    product = Product.objects.create(
        master_id=master_instance,
        ymd=ymd,
        code=productCode,
        codeName=productCodeName,
        amount=amount,
        count=count,
        amount_kg=product_Instance.amount_kg,
        memo=memo,
        productCode=product_Instance,
        purchaseYmd = purchaseYmd,
        purchaseLocation = purchaseLocation,
        purchaseLocationName=purchaseLocationName,
        purchaseSupplyPrice=purchaseSupplyPrice,
        purchaseVat=purchaseVat
    )
    ProductAdmin.objects.create(
        product_id=product,
        amount=amount,
        count=count,
        ymd=ymd,
        location=Location.objects.get(code='00301')
    )

print('productOEM 완료')