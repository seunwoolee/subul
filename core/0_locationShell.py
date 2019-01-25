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

con = cx_Oracle.connect('system/kcerp@112.216.66.219/kcerp')
cursor = con.cursor()
query = " select \
                코드 as code ,\
                이름 as codeName,\
                구분 as type,\
                주소 as location_address,\
                전화 as location_phone,\
                담당자 as location_owner,\
                사업자번호 as  location_companyNumber, \
                쇼핑몰 as location_shoppingmall, \
                분류 as location_character,\
                사용유무 as delete_state,  \
                담당직원 as locatoin_manager \
            from KCFEED.FRESH장소CD"
cursor.execute(query)
Location.objects.all().delete()
for row in cursor:
    print(row)
    delete_state = 'N' if row[9] == 'Y' else 'Y'
    user = row[10]
    user_object = ''
    if user:
        user_object = CustomUser.objects.filter(username=user).first()

    location = Location.objects.create(
        code=row[0],
        codeName=row[1],
        type=row[2],
        location_address=row[3],
        location_phone=row[4],
        location_owner=row[5],
        location_companyNumber=row[6],
        location_shoppingmall=row[7],
        location_character=row[8],
        delete_state=delete_state
    )

    if user_object:
        location.location_manager = user_object
    location.save()

print('Location 완료')