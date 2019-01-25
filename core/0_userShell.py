import os

import cx_Oracle

from core.models import Location
from eggs.models import EggCode

# cx_Oracle 한글처리 시작
from users.models import CustomUser

os.environ["NLS_LANG"] = ".AL32UTF8"
START_VALUE = u"Unicode \u3042 3".encode('utf-8')
END_VALUE = u"Unicode \u3042 6".encode('utf-8')
# cx_Oracle 한글처리 끝

con = cx_Oracle.connect('system/kcerp@155.1.19.2/kcerp')
cursor = con.cursor()
query = " select * FROM KCFEED.FUSERS"
cursor.execute(query)


for row in cursor:
    print(row)
    is_active = True if row[8] == '0' else False
    CustomUser.objects.create(
        username=row[0],
        first_name=row[2],
        is_active=is_active,
    )

admin = CustomUser.objects.get(username='admin')

for ele in CustomUser.objects.all():
    ele.password = admin.password
    ele.save()

print('user 완료')