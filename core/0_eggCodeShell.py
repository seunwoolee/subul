import os

import cx_Oracle

from core.models import Location
from eggs.models import EggCode

# cx_Oracle 한글처리 시작
os.environ["NLS_LANG"] = ".AL32UTF8"
START_VALUE = u"Unicode \u3042 3".encode('utf-8')
END_VALUE = u"Unicode \u3042 6".encode('utf-8')
# cx_Oracle 한글처리 끝

con = cx_Oracle.connect('system/kcerp@112.216.66.219/kcerp')
cursor = con.cursor()
query = " select * FROM KCFEED.FRESHCD2 "
cursor.execute(query)

for row in cursor:
    delete_state = row[6]
    if delete_state == 'N':  # 사용유무가 N이면 삭제 나머지 다 사용
        delete_state = 'Y'
    else:
        delete_state = 'N'

    EggCode.objects.create(
        code=row[0],
        codeName=row[1],
        type=row[2],
        size=row[3],
        delete_state=delete_state
    )

print('EggCode 완료')