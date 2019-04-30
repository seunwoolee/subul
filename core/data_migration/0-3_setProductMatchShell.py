import os

import cx_Oracle
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "subul.settings")
django.setup()

# cx_Oracle 한글처리 시작
from core.models import Location
from product.models import ProductCode, ProductUnitPrice, SetProductCode, SetProductMatch

os.environ["NLS_LANG"] = ".AL32UTF8"
START_VALUE = u"Unicode \u3042 3".encode('utf-8')
END_VALUE = u"Unicode \u3042 6".encode('utf-8')
# cx_Oracle 한글처리 끝

con = cx_Oracle.connect('system/kcerp@155.1.19.2/kcerp')
cursor = con.cursor()
query = " select * from KCFEED.FRESHCP "
cursor.execute(query)

for row in cursor:
    print(row)
    delete_state = 'N' if row[6] == 'Y' else 'Y'
    location = Location.objects.filter(code=row[5]).first()
    product = ProductCode.objects.filter(code=row[1]).first()
    setProduct = SetProductCode.objects.filter(code=row[0]).first()

    if location and product and setProduct:
        SetProductMatch.objects.create(
            setProductCode=setProduct,
            productCode=product,
            count=row[3],
            price=row[2],
            saleLocation=location,
            delete_state=delete_state
        )
print('setProductMatchShell 완료')