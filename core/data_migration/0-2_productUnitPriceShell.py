import os

import cx_Oracle

# cx_Oracle 한글처리 시작
from core.models import Location
from product.models import ProductCode, ProductUnitPrice

os.environ["NLS_LANG"] = ".AL32UTF8"
START_VALUE = u"Unicode \u3042 3".encode('utf-8')
END_VALUE = u"Unicode \u3042 6".encode('utf-8')
# cx_Oracle 한글처리 끝

con = cx_Oracle.connect('system/kcerp@112.216.66.219/kcerp')
cursor = con.cursor()
query = " select 거래처 as location , 제품 as product, 금액 as price , 사용유무 as delete_state from  KCFEED.FRESH단가"
cursor.execute(query)

for row in cursor:
    location = Location.objects.filter(code=row[0]).first()
    product = ProductCode.objects.filter(code=row[1]).first()
    price = row[2]
    delete_state = 'N' if row[3] == 'Y' else 'Y'

    if location and product:
        ProductUnitPrice.objects.create(
            locationCode=location,
            productCode=product,
            price=price,
            delete_state=delete_state
        )
    else:
        print(row)

print('productUnitPriceShell 완료')