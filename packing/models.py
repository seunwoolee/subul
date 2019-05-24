from django.db import models
from django.db.models import Q, F, Sum, Func
from model_utils import Choices
from core.models import Detail, Location, Code, DELETE_STATE_CHOICES
from order.models import ABS
from product.models import ProductCode


class PackingCode(Code):
    PACKING_TYPE_CHOICES = (
        ('포장재', '포장재'),
        ('외포장재', '외포장재'),
    )

    type = models.CharField(max_length=255, choices=PACKING_TYPE_CHOICES)
    size = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.codeName + '(' + self.code + ')'


class Packing(Detail):
    PACKING_TYPE_CHOICES = (
        ('입고', '입고'),
        ('생산', '생산'),
        ('폐기', '폐기'),
        ('조정', '조정'),
    )
    AUTO_TYPE_CHOICES = (
        ('자동출고', '자동출고'),
        ('수동출고', '수동출고'),
    )
    type = models.CharField(
        max_length=10,
        choices=PACKING_TYPE_CHOICES,
        default="입고"
    )
    price = models.IntegerField(null=True, blank=True)
    locationCode = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    locationCodeName = models.CharField(max_length=255, null=True, blank=True)
    packingCode = models.ForeignKey(PackingCode, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.CharField(max_length=10, null=True, blank=True)
    autoRelease = models.CharField(
        max_length=10,
        choices=AUTO_TYPE_CHOICES,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.codeName + '(' + self.ymd + ') ' + self.type

    @staticmethod
    def packingQuery(**kwargs):

        ORDER_COLUMN_CHOICES = Choices(
            ('0', 'packing_codeName'),
            ('1', 'totalCount'),
        )
        draw = int(kwargs.get('draw', None)[0])
        search_value = kwargs.get('search[value]', None)[0]
        order_column = kwargs.get('order[0][column]', None)[0]
        order = kwargs.get('order[0][dir]', None)[0]
        order_column = ORDER_COLUMN_CHOICES[order_column]

        queryset = Packing.objects.values('code', packing_codeName=F('codeName')) \
            .annotate(totalCount=Sum('count')).filter(totalCount__gt=0)

        # django orm '-' -> desc
        if order == 'desc':
            order_column = '-' + order_column

        total = queryset.count()  # TODO 삭제

        if search_value:
            queryset = queryset.filter(Q(codeName__icontains=search_value))

        count = queryset.count()  # TODO 삭제
        queryset = queryset.order_by(order_column)
        return {
            'items': queryset,
            'count': count,
            'total': total,
            'draw': draw
        }

    @staticmethod
    def packingListQuery(**kwargs):

        ORDER_COLUMN_CHOICES = Choices(
            ('0', 'id'),
            ('1', 'type'),
            ('2', 'ymd'),
            ('3', 'code'),
            ('4', 'codeName'),
            ('5', 'locationCode_code'),
            ('6', 'locationCodeName'),
            ('7', 'counts'),
            ('8', 'price'),
            ('9', 'memo'),
            ('10', 'autoRelease'),
        )
        draw = int(kwargs.get('draw', None)[0])
        start = int(kwargs.get('start', None)[0])
        length = int(kwargs.get('length', None)[0])
        search_value = kwargs.get('search[value]', None)[0]
        order_column = kwargs.get('order[0][column]', None)[0]
        order = kwargs.get('order[0][dir]', None)[0]
        order_column = ORDER_COLUMN_CHOICES[order_column]
        start_date = kwargs.get('start_date', None)[0]
        end_date = kwargs.get('end_date', None)[0]
        releaseTypeFilter = kwargs.get('releaseTypeFilter', None)[0]
        productTypeFilter = kwargs.get('productTypeFilter', None)[0]
        locatoinTypeFilter = kwargs.get('locatoinTypeFilter', None)[0]

        queryset = Packing.objects.all().annotate(locationCode_code=F('locationCode__code')) \
            .annotate(counts=ABS(F('count'))) \
            .filter(ymd__gte=start_date).filter(ymd__lte=end_date)

        total = queryset.count()

        if releaseTypeFilter != '전체':
            queryset = queryset.filter(type=releaseTypeFilter)

        if productTypeFilter:
            queryset = queryset.filter(code=productTypeFilter)

        if locatoinTypeFilter:
            queryset = queryset.filter(locationCode__code=locatoinTypeFilter)

        if order == 'desc':
            order_column = '-' + order_column

        if search_value:
            queryset = queryset.filter(
                Q(codeName__icontains=search_value) | Q(locationCodeName__icontains=search_value))

        count = queryset.count()
        if length != -1:
            queryset = queryset.order_by(order_column)[start:start + length]
        else:
            queryset = queryset.order_by(order_column)
        return {
            'items': queryset,
            'count': count,
            'total': total,
            'draw': draw
        }

    @staticmethod
    def packingReportQuery(**kwargs):
        ORDER_COLUMN_CHOICES = Choices(
            ('0', 'codeName'),
            ('1', 'previousStock'),
            ('2', 'in'),
            ('3', 'in_price'),
            ('4', 'insert'),
            ('5', 'loss'),
            ('6', 'release'),
            ('7', 'adjust'),
            ('8', 'currentStock')
        )
        draw = int(kwargs.get('draw', None)[0])
        search_value = kwargs.get('search[value]', None)[0]
        order_column = kwargs.get('order[0][column]', None)[0]
        order = kwargs.get('order[0][dir]', None)[0]
        order_column = ORDER_COLUMN_CHOICES[order_column]
        start_date = kwargs.get('start_date', None)[0]
        end_date = kwargs.get('end_date', None)[0]
        arr = []

        packing_previous: Packing = Packing.objects.values('code', 'codeName') \
            .annotate(totalCount=Sum('count')) \
            .filter(ymd__lt=start_date) \
            .filter(totalCount__gt=0)  # 재고가 0초과인 이전 재고

        if search_value:
            packing_previous = packing_previous.filter(codeName__icontains=search_value)

        for previous in packing_previous:  # 기간 내 전일재고의 각 타입별(IN, SALE, LOSS, INSERT) count를 구한다
            result = {}
            countPerType = Packing.objects.values('code', 'codeName', 'type') \
                .annotate(totalCount=Sum('count')) \
                .filter(code=previous['code']) \
                .filter(ymd__gte=start_date) \
                .filter(ymd__lte=end_date)
            PREVIOUS_STOCK = previous["totalCount"]
            INSERT = 0
            LOSS = 0
            ADJUST = 0
            for element in countPerType:  # 전일재고니깐 생성 없음
                number = element["totalCount"]
                if element['type'] == '생산':
                    INSERT += number
                elif element['type'] == '폐기':
                    LOSS += number
                elif element['type'] == '조정':
                    ADJUST += number

            RELEASE = LOSS + INSERT
            CURRENT_STOCK = PREVIOUS_STOCK + RELEASE + ADJUST
            if LOSS == 0: LOSS = None
            if INSERT == 0: INSERT = None
            if RELEASE == 0: RELEASE = None
            if ADJUST == 0: ADJUST = None
            result['codeName'] = previous['codeName']
            result['previousStock'] = PREVIOUS_STOCK
            result['in'] = None
            result['in_price'] = None
            result['loss'] = LOSS
            result['insert'] = INSERT
            result['release'] = RELEASE
            result['adjust'] = ADJUST
            result['currentStock'] = CURRENT_STOCK
            arr.append(result)

        # 기간 내 생산되고 출고된 것들의 현재고 구하기(전일재고 당연히 없음)
        packing_period = Packing.objects.values('code', 'codeName') \
            .annotate(totalCount=Sum('count')) \
            .filter(ymd__gte=start_date) \
            .filter(ymd__lte=end_date) \
            .filter(type='입고')

        if search_value:
            packing_period = packing_period.filter(codeName__icontains=search_value)

        for period in packing_period:  # 기간 내 생성된 각 타입별(IN, SALE, LOSS, INSERT) count를 구한다
            result = {}
            countPerType = Packing.objects.values('code', 'codeName', 'type') \
                .annotate(totalCount=Sum('count')) \
                .annotate(totalPrice=Sum('price')) \
                .filter(code=period['code']) \
                .filter(ymd__gte=start_date) \
                .filter(ymd__lte=end_date)
            IN = 0
            IN_PRICE = 0
            LOSS = 0
            INSERT = 0
            ADJUST = 0
            for element in countPerType:  # 전일재고니깐 생성 없음
                number = element["totalCount"]
                price = element["totalPrice"]
                if element['type'] == '입고':
                    IN += number
                    if price:
                        IN_PRICE += price
                elif element['type'] == '폐기':
                    LOSS += number
                elif element['type'] == '생산':
                    INSERT += number
                elif element['type'] == '조정':
                    ADJUST += number

            RELEASE = LOSS + INSERT
            CURRENT_STOCK = IN + RELEASE + ADJUST
            if IN == 0: IN = None
            if IN_PRICE == 0: IN_PRICE = None
            if LOSS == 0: LOSS = None
            if INSERT == 0: INSERT = None
            if RELEASE == 0: RELEASE = None
            if ADJUST == 0: ADJUST = None
            result['codeName'] = period['codeName']
            result['previousStock'] = None
            result['in'] = IN
            result['in_price'] = IN_PRICE
            result['loss'] = LOSS
            result['insert'] = INSERT
            result['release'] = RELEASE
            result['adjust'] = ADJUST
            result['currentStock'] = CURRENT_STOCK
            arr.append(result)

        arr: list = sorted(arr, key=lambda k: k['codeName'])
        temp: list = [item['codeName'] for item in arr]

        if len(temp) != len(set(temp)):
            for i in range(len(arr)):
                if len(arr) > i + 1 and arr[i]['codeName'] == arr[i + 1]['codeName']:
                    pass
                    if not arr[i]['previousStock']:
                        arr[i]['previousStock'] = arr[i + 1]['previousStock']
                    if not arr[i]['in']:
                        arr[i]['in'] = arr[i + 1]['in']
                    if not arr[i]['in_price']:
                        arr[i]['in_price'] = arr[i + 1]['in_price']
                    arr[i]['currentStock'] = arr[i]['previousStock'] + arr[i]['in'] + int(arr[i]['release'] or 0)
                    arr.pop(i + 1)
                else:
                    continue

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


class AutoPacking(models.Model):
    productCode = models.ForeignKey(ProductCode, on_delete=models.CASCADE, related_name='+')
    packingCode = models.ForeignKey(PackingCode, on_delete=models.CASCADE, related_name='+')
    count = models.IntegerField()

    def __str__(self):
        return f"자동출고 {self.productCode.codeName}_ {self.packingCode.codeName}_{self.count}개"

    @staticmethod
    def autoPackingQuery(**kwargs) -> object:

        ORDER_COLUMN_CHOICES = Choices(
            ('0', 'id'),
            ('1', 'packingCode'),
            ('2', 'packingCodeName'),
            ('3', 'productCode'),
            ('4', 'productCodeName'),
            ('5', 'count'),
        )
        draw = int(kwargs.get('draw', None)[0])
        start = int(kwargs.get('start', None)[0])
        length = int(kwargs.get('length', None)[0])
        search_value = kwargs.get('search[value]', None)[0]
        order_column = kwargs.get('order[0][column]', None)[0]
        order = kwargs.get('order[0][dir]', None)[0]
        order_column = ORDER_COLUMN_CHOICES[order_column]
        packingCode = kwargs.get('packing', None)[0]
        productCode = kwargs.get('product', None)[0]

        queryset = AutoPacking.objects.annotate(
            packingCodeName=F('packingCode__codeName'),
            productCodeName=F('productCode__codeName'))

        if packingCode:
            queryset = queryset.filter(packingCode=PackingCode.objects.get(id=packingCode))

        if productCode:
            queryset = queryset.filter(productCode=ProductCode.objects.get(id=productCode))

        if order == 'desc':
            order_column = '-' + order_column

        total = queryset.count()

        count = queryset.count()

        queryset = queryset.order_by(order_column)[start:start + length]
        return {
            'items': queryset,
            'count': count,
            'total': total,
            'draw': draw
        }