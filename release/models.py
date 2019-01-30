from django.db import models
from django.db.models import Q, F, ExpressionWrapper, Sum, DecimalField, When, Case
from django.db.models.functions import Cast
from model_utils import Choices

from core.models import Master, Detail, Location


class Release(Detail):
    RELEASE_TYPE_CHOICES = (
        ('판매', '판매'),
        ('샘플', '샘플'),
        ('증정', '증정'),
        ('자손', '자손'),
        ('반품', '반품'),
        ('이동', '이동'),
        ('재고조정', '재고조정'),
    )

    SPECIALTAG_TYPE_CHOICES = (
        ('', '일반'),
        ('특인가', '특인가'),
    )

    type = models.CharField(
        max_length=10,
        choices=RELEASE_TYPE_CHOICES,
        default='판매',
    )
    product_id = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='product', null=True,
                                   blank=True)
    productYmd = models.CharField(max_length=8)
    releaseLocationCode = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='release_locationCode')
    releaseLocationName = models.CharField(max_length=255)
    price = models.IntegerField()
    releaseOrder = models.ForeignKey('order.Order', on_delete=models.CASCADE, null=True, blank=True)
    releaseStoreLocation = models.ForeignKey(Location, on_delete=models.CASCADE,
                                             related_name='release_releaseStoreLocation')
    releaseSetProductCode = models.ForeignKey('product.SetProductCode', on_delete=models.CASCADE, null=True, blank=True)
    releaseVat = models.IntegerField()
    specialTag = models.CharField(
        max_length=10,
        choices=SPECIALTAG_TYPE_CHOICES,
        default='',
        blank=True
    )

    def __str__(self):
        return f"{self.codeName}_{self.type}_{self.releaseLocationName}"

    @staticmethod
    def releaseQuery(**kwargs):
        draw = int(kwargs.get('draw', None)[0])
        start = int(kwargs.get('start', None)[0])
        length = int(kwargs.get('length', None)[0])
        search_value = kwargs.get('search[value]', None)[0]
        start_date = kwargs.get('start_date', None)[0]
        end_date = kwargs.get('end_date', None)[0]
        order_column = kwargs.get('order[0][column]', None)[0]
        order = kwargs.get('order[0][dir]', None)[0]
        releaseTypeFilter = kwargs.get('releaseTypeFilter', None)[0]
        productTypeFilter = kwargs.get('productTypeFilter', None)[0]
        groupByFilter = kwargs.get('groupByFilter', None)[0]
        checkBoxFilter = kwargs.get('checkBoxFilter', None)[0]
        location_manager = kwargs.get('location_manager', None)[0]
        user_instance = kwargs.get("user_instance", None)[0]
        if checkBoxFilter: checkBoxFilter = checkBoxFilter.split(',')

        if groupByFilter == 'stepOne':
            RELEASE_COLUMN_CHOICES = Choices(
                ('0', 'id'),
                ('1', 'ymd'),
                ('2', 'releaseLocationName'),
                ('3', 'contentType'),
                ('4', 'specialTag'),
                ('5', 'code'),
                ('6', 'codeName'),
                ('7', 'amount'),
                ('8', 'count'),
                ('9', 'kgPrice'),
                ('10', 'totalPrice'),
                ('11', 'supplyPrice'),
                ('12', 'releaseVat'),
                ('13', 'eaPrice'),
                ('14', 'productYmd'),
                ('15', 'type'),
                ('16', 'releaseStoreLocationCodeName'),
                ('17', 'orderMemo'),
                ('18', 'memo'),
                ('19', 'locationType'),
                ('20', 'locationManagerName'),
                ('21', 'releaseSetProduct'),
                ('22', 'releaseSetProductCodeName'),
            )
            order_column = RELEASE_COLUMN_CHOICES[order_column]
            queryset = Release.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date) \
                .annotate(kgPrice=Case(
                When(price=0, then=0),
                When(amount=0, then=0),
                default=ExpressionWrapper(F('price') / F('amount'), output_field=DecimalField()))) \
                .annotate(contentType=F('product_id__productCode__type')) \
                .annotate(totalPrice=F('price')) \
                .annotate(supplyPrice=ExpressionWrapper(F('price') - F('releaseVat'), output_field=DecimalField())) \
                .annotate(eaPrice=Case(
                When(price=0, then=0),
                When(count=0, then=0),
                default=ExpressionWrapper(F('price') / F('count'), output_field=DecimalField()))) \
                .annotate(releaseStoreLocationCodeName=F('releaseStoreLocation__codeName')) \
                .annotate(orderMemo=F('releaseOrder__memo')) \
                .annotate(locationType=F('releaseLocationCode__location_character')) \
                .annotate(locationManagerName=F('releaseLocationCode__location_manager__first_name')) \
                .annotate(releaseSetProduct=F('releaseSetProductCode__code')) \
                .annotate(releaseSetProductCodeName=F('releaseSetProductCode__codeName'))
        elif groupByFilter == 'stepTwo':
            RELEASE_COLUMN_CHOICES = Choices(
                ('0', 'code'),
                ('1', 'specialTag'),
                ('2', 'codeName'),
                ('3', "type"),
                ('4', 'contentType'),
                ('5', 'amount'),
                ('6', 'count'),
                ('7', 'totalPrice'),
                ('8', 'kgPrice'),
                ('9', 'supplyPrice'),
                ('10', 'releaseVat'),
                ('11', "eaPrice"),
                ('12', "releaseStoreLocationCodeName")
            )
            order_column = RELEASE_COLUMN_CHOICES[order_column]
            queryset = Release.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date) \
                .filter(delete_state='N') \
                .values('code', 'codeName', 'type', 'specialTag') \
                .annotate(contentType=F('product_id__productCode__type')) \
                .annotate(amount=Sum('amount')) \
                .annotate(count=Sum('count')) \
                .annotate(totalPrice=Sum('price')) \
                .annotate(releaseVat=Sum('releaseVat')) \
                .annotate(releaseStoreLocationCodeName=F('releaseStoreLocation__codeName'))

            queryset = queryset.annotate(eaPrice=Case(When(totalPrice=0, then=0), default=F('totalPrice') / F('count'))) \
                .annotate(supplyPrice=ExpressionWrapper(F('totalPrice') - F('releaseVat'), output_field=DecimalField())) \
                .annotate(kgPrice=ExpressionWrapper(F('totalPrice') / F('amount'), output_field=DecimalField()))

        elif groupByFilter == 'stepThree':
            RELEASE_COLUMN_CHOICES = Choices(
                ('0', 'code'),
                ('1', 'specialTag'),
                ('2', 'codeName'),
                ('3', "type"),
                ('4', "releaseLocationName"),
                ('5', 'contentType'),
                ('6', 'amount'),
                ('7', 'count'),
                ('8', 'totalPrice'),
                ('9', 'kgPrice'),
                ('10', 'supplyPrice'),
                ('11', 'releaseVat'),
                ('12', "eaPrice"),
                ('13', "releaseStoreLocationCodeName")
            )
            order_column = RELEASE_COLUMN_CHOICES[order_column]
            queryset = Release.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date).filter(delete_state='N') \
                .values('code', 'codeName', 'type', 'specialTag') \
                .annotate(contentType=F('product_id__productCode__type')) \
                .annotate(releaseLocationName=F('releaseLocationName')) \
                .annotate(amount=Sum('amount')) \
                .annotate(count=Sum('count')) \
                .annotate(releaseVat=Sum('releaseVat')) \
                .annotate(totalPrice=Sum('price')) \
                .annotate(releaseStoreLocationCodeName=F('releaseStoreLocation__codeName'))

            queryset = queryset.annotate(eaPrice=Case(When(totalPrice=0, then=0), default=F('totalPrice') / F('count'))) \
                .annotate(supplyPrice=ExpressionWrapper(F('totalPrice') - F('releaseVat'), output_field=DecimalField())) \
                .annotate(kgPrice=ExpressionWrapper(F('totalPrice') / F('amount'), output_field=DecimalField()))

        elif groupByFilter == 'stepFour':
            RELEASE_COLUMN_CHOICES = Choices(
                ('0', 'releaseLocationName'),
                ('1', 'amount'),
                ('2', "count"),
                ('3', 'totalPrice'),
                ('4', 'supplyPrice'),
                ('5', 'releaseVat'),
            )
            order_column = RELEASE_COLUMN_CHOICES[order_column]
            queryset = Release.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date) \
                .filter(delete_state='N') \
                .values('releaseLocationName') \
                .annotate(amount=Sum('amount')) \
                .annotate(count=Sum('count')) \
                .annotate(totalPrice=Sum('price')) \
                .annotate(releaseVat=Sum('releaseVat')) \
                .annotate(supplyPrice=F('totalPrice') - F('releaseVat'))
        elif groupByFilter == 'stepFive':
            from django.apps import apps
            ProductAdmin = apps.get_model('product', 'ProductAdmin')
            ProductEgg = apps.get_model('product', 'ProductEgg')
            RELEASE_COLUMN_CHOICES = {
                '0': 'id',
                '1': 'code',
                '2': 'codeName',
                '3': 'ymd',
                '4': 'previousStock',
                '5': 'in',
                '6': 'sale',
                '7': 'sample',
                '8': 'broken',
                '9': 'notProduct',
                '10': 'recall',
                '11': 'currentStock'
            }
            order_column = RELEASE_COLUMN_CHOICES[order_column]
            arr = []

            productAdmin_previous = ProductAdmin.objects.values(  # 전일재고
                productId=F('product_id__id'),
                productCode=F('product_id__code'),
                productCodeName=F('product_id__codeName'),
                productYmd=F('product_id__ymd')) \
                .annotate(totalCount=Sum('count')).annotate(totalAmount=Sum('amount')) \
                .filter(ymd__lt=start_date).filter(totalCount__gt=0).filter(totalAmount__gt=0)  # 재고가 0초과인 이전 재고

            if search_value:
                productAdmin_previous = productAdmin_previous.filter(productCodeName__icontains=search_value)

            for previous in productAdmin_previous:  # 기간 내 전일재고의 각 타입별 amount를 구한다
                result = {}
                countPerType = ProductAdmin.objects.values(productCode=F('product_id__code'),  # 타입별 출고 amount
                                                           productCodeName=F('product_id__codeName'),
                                                           productYmd=F('product_id__ymd'), type=F('releaseType')) \
                    .annotate(totalCount=Sum('count')) \
                    .annotate(totalAmount=Sum('amount')) \
                    .filter(product_id=previous['productId']).filter(ymd__gte=start_date).filter(ymd__lte=end_date)

                PREVIOUS_STOCK = previous['totalAmount']
                SALE = 0
                SAMPLE = 0
                BROKEN = 0
                NOTPRODUCT = 0
                RECALL = 0

                for element in countPerType:  # 전일재고니깐 생성 없음
                    number = element["totalAmount"]
                    if element['type'] == '판매':
                        SALE += number
                    elif element['type'] == '샘플' or element['type'] == '증정':
                        SAMPLE += number
                    elif element['type'] == '자손':
                        BROKEN += number
                    elif element['type'] == '미출고품사용':
                        NOTPRODUCT += number
                    elif element['type'] == '반품':
                        RECALL += number
                CURRENT_STOCK = PREVIOUS_STOCK + SALE + SAMPLE + BROKEN + NOTPRODUCT + RECALL
                if SALE == 0: SALE = None
                if SAMPLE == 0: SAMPLE = None
                if BROKEN == 0: BROKEN = None
                if NOTPRODUCT == 0: NOTPRODUCT = None
                if RECALL == 0: RECALL = None
                if CURRENT_STOCK == 0: CURRENT_STOCK = None
                result['id'] = previous['productId']
                result['code'] = previous['productCode']
                result['codeName'] = previous['productCodeName']
                result['ymd'] = previous['productYmd']
                result['previousStock'] = PREVIOUS_STOCK
                result['in'] = None
                result['sale'] = SALE
                result['sample'] = SAMPLE
                result['broken'] = BROKEN
                result['notProduct'] = NOTPRODUCT
                result['recall'] = RECALL
                result['currentStock'] = CURRENT_STOCK
                arr.append(result)

            # 기간 내 생산되고 출고된 것들의 현재고 구하기(전일재고 당연히 없음)
            productAdmin_period = ProductAdmin.objects.values(productId=F('product_id__id'),
                                                              productCode=F('product_id__code'),
                                                              productCodeName=F('product_id__codeName'),
                                                              productYmd=F('product_id__ymd')) \
                .annotate(totalCount=Sum('count')) \
                .annotate(totalAmount=Sum('amount')) \
                .filter(ymd__gte=start_date).filter(ymd__lte=end_date)  # 단순히 묶기위해 Sum을함

            if search_value:
                productAdmin_period = productAdmin_period.filter(productCodeName__icontains=search_value)

            for period in productAdmin_period:
                result = {}
                countPerType = ProductAdmin.objects.values(productCode=F('product_id__code'),  # 타입별 출고 amount
                                                           productCodeName=F('product_id__codeName'),
                                                           productYmd=F('product_id__ymd'), type=F('releaseType'),
                                                           releaseInfo=F('releaseSeq__id')) \
                    .annotate(totalCount=Sum('count')) \
                    .annotate(totalAmount=Sum('amount')) \
                    .filter(product_id=period['productId']).filter(ymd__gte=start_date).filter(ymd__lte=end_date)
                IN = 0
                SALE = 0
                SAMPLE = 0
                BROKEN = 0
                NOTPRODUCT = 0
                RECALL = 0

                for element in countPerType:
                    number = element["totalAmount"]
                    if element['type'] == '생성':
                        if element['releaseInfo'] is None:  # 이동으로 인한 생성 제외
                            IN += number
                        else:
                            continue
                    elif element['type'] == '판매':
                        SALE += number
                    elif element['type'] == '샘플' or element['type'] == '증정':
                        SAMPLE += number
                    elif element['type'] == '자손':
                        BROKEN += number
                    elif element['type'] == '미출고품사용':
                        NOTPRODUCT += number
                    elif element['type'] == '반품':
                        RECALL += number

                if IN > 0:  # IN 데이터가 존재하지 않으면 위에서 계산된거임
                    CURRENT_STOCK = IN + SALE + SAMPLE + BROKEN + NOTPRODUCT + RECALL
                    if IN == 0: IN = None
                    if SALE == 0: SALE = None
                    if SAMPLE == 0: SAMPLE = None
                    if BROKEN == 0: BROKEN = None
                    if NOTPRODUCT == 0: NOTPRODUCT = None
                    if RECALL == 0: RECALL = None
                    if CURRENT_STOCK == 0: CURRENT_STOCK = None

                    result['id'] = period['productId']
                    result['code'] = period['productCode']
                    result['codeName'] = period['productCodeName']
                    result['ymd'] = period['productYmd']
                    result['previousStock'] = None
                    result['in'] = IN
                    result['sale'] = SALE
                    result['sample'] = SAMPLE
                    result['broken'] = BROKEN
                    result['notProduct'] = NOTPRODUCT
                    result['recall'] = RECALL
                    result['currentStock'] = CURRENT_STOCK
                    arr.append(result)

            # print(arr)

            # 전일 재고 액란 구하기
            tankValue_previous = ProductEgg.objects.values('code', 'codeName') \
                .filter(delete_state='N').annotate(rawSum=Sum('rawTank_amount')) \
                .annotate(pastSum=Sum('pastTank_amount')).filter(ymd__lt=start_date).order_by('code')

            if search_value:
                tankValue_previous = tankValue_previous.filter(codeName__icontains=search_value)

            for tank in tankValue_previous:
                if "RAW" in tank["codeName"]:
                    tank["amount"] = tank["rawSum"]
                elif "Past" in tank["codeName"]:
                    tank["amount"] = tank["pastSum"]

            # 기간 내 액란 구하기
            tankValue_period = ProductEgg.objects.values('code', 'codeName') \
                .filter(delete_state='N').annotate(rawSum=Sum('rawTank_amount')) \
                .annotate(pastSum=Sum('pastTank_amount')).filter(ymd__gte=start_date).filter(
                ymd__lte=end_date).order_by('code')

            if search_value:
                tankValue_period = tankValue_period.filter(codeName__icontains=search_value)

            for tank in tankValue_period:
                if "RAW" in tank["codeName"]:
                    tank["amount"] = tank["rawSum"]
                elif "Past" in tank["codeName"]:
                    tank["amount"] = tank["pastSum"]

            for eachTank in tankValue_previous:
                IN = 0
                for in_period in tankValue_period:
                    if eachTank['code'] == in_period['code']:
                        IN = in_period['amount']
                        break

                CURRENT_STOCK = eachTank['amount'] + IN
                # if IN == 0: IN = None
                # if eachTank['amount'] == 0: eachTank['amount'] = None

                result = {}
                result['id'] = 99999
                result['code'] = eachTank['code']
                result['codeName'] = eachTank['codeName']
                result['ymd'] = ''
                result['previousStock'] = eachTank['amount']
                result['in'] = IN
                result['sale'] = None
                result['sample'] = None
                result['broken'] = None
                result['notProduct'] = None
                result['recall'] = None
                result['currentStock'] = CURRENT_STOCK
                arr.append(result)

            if order == 'desc':
                arr = sorted(arr, key=lambda k: k[order_column] if k[order_column] is not None else 0, reverse=True)
            else:
                arr = sorted(arr, key=lambda k: k[order_column] if k[order_column] is not None else 0)

            return {
                'items': arr,
                'count': 10,
                'total': 10,
                'draw': draw
            }
        # elif groupByFilter == 'stepSix':
        #     from django.apps import apps
        #     ProductAdmin = apps.get_model('product', 'ProductAdmin')
        #     RELEASE_COLUMN_CHOICES = {
        #         '0': 'id',
        #         '1': 'locationCode',
        #         '2': 'locationCodeName',
        #         '3': 'productCode',
        #         '4': 'productCodeName',
        #         '5': 'ymd',
        #         '6': 'previousStock',
        #         '7': 'in',
        #         '8': 'move',
        #         '9': 'sale',
        #         '10': 'currentStock'
        #     }
        #     order_column = RELEASE_COLUMN_CHOICES[order_column]
        #     arr = []
        #
        #     productAdmin_previous = ProductAdmin.objects.values(  # 전일재고
        #         productId=F('product_id__id'),
        #         locationCode=F('location__code'),
        #         locationCodeName=F('location__codeName'),
        #         productCode=F('product_id__code'),
        #         productCodeName=F('product_id__codeName'),
        #         oem=F('product_id__productCode__oem'),
        #         productYmd=F('product_id__ymd')) \
        #         .annotate(totalCount=Sum('count')).annotate(totalAmount=Sum('amount')) \
        #         .filter(ymd__lt=start_date) \
        #         .filter(totalCount__gt=0)  # 재고가 0초과인 이전 재고
        #
        #     print(productAdmin_previous)
        #
        #     if search_value:
        #         productAdmin_previous = productAdmin_previous.filter(productCodeName__icontains=search_value)
        #
        #     for previous in productAdmin_previous:  # 기간 내 전일재고의 각 타입별(IN, SALE, MOVE) amount를 구한다
        #         result = {}
        #         countPerType = ProductAdmin.objects.values(
        #             locationCode=F('location__code'),
        #             locationCodeName=F('location__codeName'),
        #             productCode=F('product_id__code'),  # 타입별 출고 amount
        #             productCodeName=F('product_id__codeName'),
        #             productYmd=F('product_id__ymd'), type=F('releaseType')) \
        #             .annotate(totalCount=Sum('count')) \
        #             .annotate(totalAmount=Sum('amount')) \
        #             .filter(product_id=previous['productId']).filter(ymd=start_date)  # TODO 금일판매의 기준
        #
        #         PREVIOUS_STOCK = previous['totalAmount'] if previous['oem'] == 'N' else previous["totalCount"]
        #         IN = 0
        #         SALE = 0
        #         MOVE = 0
        #         for element in countPerType:
        #             if previous['locationCode'] == element['locationCode']:  # 다른 판매장소에서 이루어진 것들 제외
        #                 number = element["totalAmount"] if previous['oem'] == 'N' else element["totalCount"]
        #             else:
        #                 continue
        #             if element['type'] == '이동':
        #                 MOVE += number
        #             elif element['type'] == '생성':
        #                 IN += number
        #             else:
        #                 SALE += number
        #
        #         CURRENT_STOCK = PREVIOUS_STOCK + SALE + MOVE + IN
        #         if SALE == 0: SALE = None
        #         if MOVE == 0: MOVE = None
        #         if IN == 0: IN = None
        #         if CURRENT_STOCK == 0: CURRENT_STOCK = None
        #         result['id'] = previous['productId']
        #         result['locationCode'] = previous['locationCode']
        #         result['locationCodeName'] = previous['locationCodeName']
        #         result['productCode'] = previous['productCode']
        #         result['productCodeName'] = previous['productCodeName']
        #         result['ymd'] = previous['productYmd']
        #         result['previousStock'] = PREVIOUS_STOCK
        #         result['in'] = IN
        #         result['move'] = MOVE
        #         result['sale'] = SALE
        #         result['currentStock'] = CURRENT_STOCK
        #         arr.append(result)
        #
        #     productAdmin_period = ProductAdmin.objects.values(  # 금일 입고 또는 이동된 제품
        #         productId=F('product_id__id'),
        #         locationCode=F('location__code'),
        #         locationCodeName=F('location__codeName'),
        #         productCode=F('product_id__code'),
        #         productCodeName=F('product_id__codeName'),
        #         oem=F('product_id__productCode__oem'),
        #         productYmd=F('product_id__ymd')) \
        #         .annotate(totalCount=Sum('count')).annotate(totalAmount=Sum('amount')) \
        #         .filter(ymd=start_date)
        #
        #     print(productAdmin_period)
        #
        #     if search_value:
        #         productAdmin_period = productAdmin_period.filter(productCodeName__icontains=search_value)
        #
        #     for period in productAdmin_period:
        #         result = {}
        #         countPerType = ProductAdmin.objects.values(
        #             locationCode=F('location__code'),
        #             locationCodeName=F('location__codeName'),
        #             productCode=F('product_id__code'),  # 타입별 출고 amount
        #             productCodeName=F('product_id__codeName'),
        #             productYmd=F('product_id__ymd'), type=F('releaseType'), releaseInfo=F('releaseSeq__id')) \
        #             .annotate(totalCount=Sum('count')) \
        #             .annotate(totalAmount=Sum('amount')) \
        #             .filter(product_id=period['productId']).filter(ymd=start_date)
        #         IN = 0
        #         SALE = 0
        #         MOVE = 0
        #         for element in countPerType:
        #             if period['locationCode'] == element['locationCode']:  # 다른 판매장소에서 이루어진 것들 제외
        #                 number = element["totalAmount"] if period['oem'] == 'N' else element["totalCount"]
        #             else:
        #                 continue
        #             if element['type'] == '생성':
        #                 if element['releaseInfo'] is None:  # 이동으로 인한 생성은 이동으로 간주
        #                     IN += number
        #                 else:
        #                     MOVE += number
        #             elif element['type'] == '이동':
        #                 MOVE += number
        #             else:
        #                 SALE += number
        #         CURRENT_STOCK = SALE + MOVE + IN
        #         if IN > 0 or MOVE > 0:
        #             if SALE == 0: SALE = None
        #             if MOVE == 0: MOVE = None
        #             if IN == 0: IN = None
        #             if CURRENT_STOCK == 0: CURRENT_STOCK = None
        #             result['id'] = period['productId']
        #             result['locationCode'] = period['locationCode']
        #             result['locationCodeName'] = period['locationCodeName']
        #             result['productCode'] = period['productCode']
        #             result['productCodeName'] = period['productCodeName']
        #             result['ymd'] = period['productYmd']
        #             result['previousStock'] = None
        #             result['in'] = IN
        #             result['move'] = MOVE
        #             result['sale'] = SALE
        #             result['currentStock'] = CURRENT_STOCK
        #             arr.append(result)
        #
        #     if order == 'desc':
        #         arr = sorted(arr, key=lambda k: k[order_column] if k[order_column] is not None else 0, reverse=True)
        #     else:
        #         arr = sorted(arr, key=lambda k: k[order_column] if k[order_column] is not None else 0)
        #     return {
        #         'items': arr,
        #         'count': 10,
        #         'total': 10,
        #         'draw': draw
        #     }

        total = queryset.count()
        if releaseTypeFilter != '전체':
            queryset = queryset.filter(type=releaseTypeFilter)

        if productTypeFilter != '전체':
            queryset = queryset.filter(product_id__productCode__type=productTypeFilter)

        if checkBoxFilter:
            queryset = queryset.filter(releaseLocationCode__location_character__in=checkBoxFilter)

        if location_manager == "true":
            queryset = queryset.filter(releaseLocationCode__location_manager=user_instance)

        if order == 'desc':
            order_column = '-' + order_column

        if search_value:
            queryset = queryset.filter(Q(code__icontains=search_value) |
                                       Q(codeName__icontains=search_value) |
                                       Q(memo__icontains=search_value))

        count = queryset.count()

        if length > 0:
            queryset = queryset.order_by(order_column)[start:start + length]
        else:
            queryset = queryset.order_by(order_column)

        return {
            'items': queryset,
            'count': count,
            'total': total,
            'draw': draw
        }
