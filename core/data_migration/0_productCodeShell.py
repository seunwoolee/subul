import os

import cx_Oracle

# cx_Oracle 한글처리 시작
from product.models import ProductCode

os.environ["NLS_LANG"] = ".AL32UTF8"
START_VALUE = u"Unicode \u3042 3".encode('utf-8')
END_VALUE = u"Unicode \u3042 6".encode('utf-8')
# cx_Oracle 한글처리 끝

con = cx_Oracle.connect('system/kcerp@112.216.66.219/kcerp')
cursor = con.cursor()
query = " select \
                코드 as code ,\
                품명 as codeName,\
                내용구분 as type,\
                그램수량 as amount_kg,\
                단가 as price,\
                포장 as store_type, \
                세율 as vat, \
                유통기한 as expiration, \
                사용유무 as delete_state, \
                구분1 as OEM \
            from KCFEED.FRESHCD1"
cursor.execute(query)

for row in cursor:
    print(row)
    oem = row[9]
    type = row[2]
    if type is None:
        type = '없음'

    delete_state = row[8]
    if delete_state == 'N':  # 사용유무가 N이면 삭제 나머지 다 사용
        delete_state = 'Y'
    else:
        delete_state = 'N'

    productCode = ProductCode.objects.create(
        code=row[0],
        codeName=row[1],
        type=type,
        amount_kg=row[3],
        price=row[4],
        store_type=row[5],
        vat=row[6],
        expiration=row[7],
        delete_state=delete_state
    )

    if oem == 'O':
        productCode.oem = 'Y'
    productCode.save()


print('productCode 완료')