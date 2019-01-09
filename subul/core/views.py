import csv

from django.shortcuts import render
from django.views import View

from eggs.models import EggCode
from packing.models import PackingCode
from product.models import ProductCode, ProductUnitPrice, SetProductCode, SetProductMatch
from .models import Location

import cx_Oracle
import os

# cx_Oracle 한글처리 시작
os.environ["NLS_LANG"] = ".AL32UTF8"
START_VALUE = u"Unicode \u3042 3".encode('utf-8')
END_VALUE = u"Unicode \u3042 6".encode('utf-8')


# cx_Oracle 한글처리 끝


class LocationMigrate(View):
    def get(self, request):
        con = cx_Oracle.connect('system/kcerp@155.1.19.2/kcerp')
        cursor = con.cursor()
        query = " select \
                        코드 as code ,\
                        이름 as codeName,\
                        구분 as type,\
                        주소 as location_address,\
                        전화 as location_phone,\
                        사업자번호 as  location_companyNumber, \
                        쇼핑몰 as location_shoppingmall, \
                        분류 as location_character,\
                        사용유무 as delete_state  \
                    from KCFEED.FRESH장소CD"
        cursor.execute(query)

        for row in cursor:
            try:
                location = Location.objects.create(
                    code=row[0],
                    codeName=row[1],
                    type=row[2],
                    location_address=row[3],
                    location_phone=row[4],
                    location_companyNumber=row[5],
                    location_shoppingmall=row[6],
                    location_character=row[7],
                    delete_state=row[8]
                )
            except Exception as e:
                print(e)


class ProductCodeMigrate(View):
    def get(self, request):
        con = cx_Oracle.connect('system/kcerp@155.1.19.2/kcerp')
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
                        사용유무 as delete_state \
                    from KCFEED.FRESHCD1"
        cursor.execute(query)

        for row in cursor:
            try:

                type = row[2]
                if type is None:
                    type = '난백'

                delete_state = row[8]
                if delete_state is None:
                    delete_state = 'Y'

                location = ProductCode.objects.create(
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
            except Exception as e:
                print(e)


class ProductUnitPriceMigrate(View):
    def get(self, request):
        con = cx_Oracle.connect('system/kcerp@155.1.19.2/kcerp')
        cursor = con.cursor()
        query = " select 거래처 as location , 제품 as product, 금액 as price , 사용유무 as delete_state from  KCFEED.FRESH단가"
        cursor.execute(query)

        for row in cursor:
            try:

                location = Location.objects.get(code=row[0])
                product = ProductCode.objects.get(code=row[1])
                price = row[2]
                delete_state = row[3]

                location = ProductUnitPrice.objects.create(
                    locationCode=location,
                    productCode=product,
                    price=price,
                    delete_state=delete_state
                )
            except Exception as e:
                print(e)


class SetProductCodeMigrate(View):
    def get(self, request):
        con = cx_Oracle.connect('system/kcerp@155.1.19.2/kcerp')
        cursor = con.cursor()
        query = " select * from KCFEED.FRESHCD4 "
        cursor.execute(query)

        for row in cursor:
            try:
                location = Location.objects.get(code=row[8])

                setProductCode = SetProductCode.objects.create(
                    code=row[0],
                    codeName=row[1],
                    type='세트상품',
                    location=location,
                    delete_state=row[3]
                )
            except Exception as e:
                print(e)


class SetProductMatchMigrate(View):
    def get(self, request):
        con = cx_Oracle.connect('system/kcerp@155.1.19.2/kcerp')
        cursor = con.cursor()
        query = " select * from KCFEED.FRESHCP "
        cursor.execute(query)

        for row in cursor:
            try:
                location = Location.objects.get(code=row[5])
                product = ProductCode.objects.get(code=row[1])
                setProduct = SetProductCode.objects.get(code=row[0])

                setProductCode = SetProductMatch.objects.create(
                    setProductCode=setProduct,
                    productCode=product,
                    count=row[3],
                    price=row[2],
                    saleLocation=location,
                    delete_state=row[6]
                )
            except Exception as e:
                print(e)


class EggCodeMigrate(View):
    def get(self, request):
        con = cx_Oracle.connect('system/kcerp@155.1.19.2/kcerp')
        cursor = con.cursor()
        query = " select * FROM KCFEED.FRESHCD2 "
        cursor.execute(query)

        for row in cursor:
            delete_state = row[6]
            if delete_state is None:
                delete_state = 'Y'

            EggCode.objects.create(
                code=row[0],
                codeName=row[1],
                type=row[2],
                size=row[3],
                delete_state=delete_state
            )


class PackingCodeMigrate(View):
    def get(self, request):
        con = cx_Oracle.connect('system/kcerp@155.1.19.2/kcerp')
        cursor = con.cursor()
        query = " select * FROM KCFEED.FRESHCD "
        cursor.execute(query)

        for row in cursor:
            delete_state = row[6]
            if delete_state is None:
                delete_state = 'Y'

            PackingCode.objects.create(
                code=row[0],
                codeName=row[3],
                type=row[2],
                size=row[4],
                delete_state=delete_state
            )


class ProductMasterMigrate(View):
    def get(self, request):
        con = cx_Oracle.connect('system/kcerp@155.1.19.2/kcerp')
        cursor = con.cursor()
        query = " select * FROM KCFEED.FRESHCD "
        cursor.execute(query)

        for row in cursor:
            delete_state = row[6]
            if delete_state is None:
                delete_state = 'Y'

            PackingCode.objects.create(
                code=row[0],
                codeName=row[3],
                type=row[2],
                size=row[4],
                delete_state=delete_state
            )
