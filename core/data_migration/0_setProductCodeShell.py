import os

import cx_Oracle

# cx_Oracle 한글처리 시작
from core.models import Location
from product.models import ProductCode, ProductUnitPrice, SetProductCode

os.environ["NLS_LANG"] = ".AL32UTF8"
START_VALUE = u"Unicode \u3042 3".encode('utf-8')
END_VALUE = u"Unicode \u3042 6".encode('utf-8')
# cx_Oracle 한글처리 끝

con = cx_Oracle.connect('system/kcerp@112.216.66.219/kcerp')
cursor = con.cursor()
query = " select * from KCFEED.FRESHCD4 "
cursor.execute(query)

for row in cursor:
    print(row)
    delete_state = 'N' if row[3] == 'Y' else 'Y'
    location = Location.objects.filter(code=row[8]).first()

    if location:
        SetProductCode.objects.create(
            code=row[0],
            codeName=row[1],
            type='세트상품',
            location=location,
            delete_state=delete_state
        )

print('SetProductCodeShell 완료')