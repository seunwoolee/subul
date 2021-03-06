import os

import cx_Oracle
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "subul.settings")
django.setup()

from core.models import Location
from eggs.models import EggCode

# cx_Oracle 한글처리 시작
from packing.models import PackingCode

os.environ["NLS_LANG"] = ".AL32UTF8"
START_VALUE = u"Unicode \u3042 3".encode('utf-8')
END_VALUE = u"Unicode \u3042 6".encode('utf-8')
# cx_Oracle 한글처리 끝

con = cx_Oracle.connect('system/kcerp@155.1.19.2/kcerp')
cursor = con.cursor()
query = " select * FROM KCFEED.FRESHCD "
cursor.execute(query)

for row in cursor:
    print(row)
    delete_state = row[6]
    if delete_state == 'N':  # 사용유무가 N이면 삭제 나머지 다 사용
        delete_state = 'Y'
    else:
        delete_state = 'N'

    PackingCode.objects.create(
        code=row[0],
        codeName=row[3],
        type=row[2],
        size=row[4],
        delete_state=delete_state
    )
print('PackingCode 완료')