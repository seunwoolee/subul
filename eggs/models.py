from django.db import models
from django.db.models import Sum, DecimalField, F, Q, FloatField, Func, Value, IntegerField, Case, When, \
    ExpressionWrapper
from django.db.models.functions import Cast
from model_utils import Choices
from core.models import Detail, Location, Code


class ABS(Func):
    function = 'ABS'


class EggCode(Code):
    type = models.CharField(max_length=255, null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.codeName + '(' + self.code + ')'


class Egg(Detail):
    EGG_TYPE_CHOICES = (
        ('입고', '입고'),
        ('생산', '생산'),
        ('폐기', '폐기'),
        ('판매', '판매'),
    )
    type = models.CharField(
        max_length=10,
        choices=EGG_TYPE_CHOICES,
        default='입고',
    )
    in_locationCode = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True,
                                        related_name='in_location')
    in_locationCodeName = models.CharField(max_length=255, null=True, blank=True)
    in_ymd = models.CharField(max_length=8, null=True, blank=True)
    ymd = models.CharField(max_length=8, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    locationCode = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    locationCodeName = models.CharField(max_length=255, null=True, blank=True)
    eggCode = models.ForeignKey(EggCode, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=19, null=True, blank=True)

    def __str__(self):
        return self.codeName + '(' + self.in_ymd + ') ' + self.type + '_' + self.in_locationCodeName

    @staticmethod
    def eggQuery(**kwargs):

        ORDER_COLUMN_CHOICES = Choices(
            ('0', 'egg_in_locationCodeName'),
            ('1', 'egg_codeName'),
            ('2', 'egg_in_ymd'),
            ('3', 'totalCount'),
        )
        draw = int(kwargs.get('draw', None)[0])
        search_value = kwargs.get('search[value]', None)[0]
        order_column = kwargs.get('order[0][column]', None)[0]
        order = kwargs.get('order[0][dir]', None)[0]
        order_column = ORDER_COLUMN_CHOICES[order_column]

        queryset = Egg.objects.values(egg_in_locationCode=F('in_locationCode__code'),
                                      egg_in_locationCodeName=F('in_locationCode__codeName'),
                                      egg_code=F('code'),
                                      egg_codeName=F('codeName'),
                                      egg_in_ymd=F('in_ymd')).annotate(totalCount=Sum('count')).filter(totalCount__gt=0)

        if order == 'desc':
            order_column = '-' + order_column

        total = queryset.count()

        if search_value:
            queryset = queryset.filter(Q(codeName__icontains=search_value) |
                                       Q(egg_in_locationCodeName__icontains=search_value))

        count = queryset.count()
        queryset = queryset.order_by(order_column)
        return {
            'items': queryset,
            'count': count,
            'total': total,
            'draw': draw
        }

    @staticmethod
    def eggListQuery(**kwargs):

        ORDER_COLUMN_CHOICES = Choices(
            ('0', 'id'),
            ('1', 'type'),
            ('2', 'in_ymd'),
            ('3', 'codeName'),
            ('4', 'in_locationCodeName'),
            ('5', 'locationCodeName'),
            ('6', 'ymd'),
            ('7', 'counts'),
            ('8', 'amount'),
            ('9', 'in_price'),
            ('10', 'out_price'),
            ('11', 'pricePerEa'),
            ('12', 'memo'),
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

        queryset = Egg.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date) \
            .annotate(counts=ABS(F('count'))) \
            .annotate(in_locationCodes=F('in_locationCode__code')) \
            .annotate(in_price=Case(When(type='입고', then=F('price')),  default=0))\
            .annotate(out_price=Case(When(type='판매', then=F('price')),  default=0))\
            .annotate(pricePerEa=Case(When(price=0, then=0), When(count=0, then=0), default=F('price') / ABS(F('count'))))

        queryset = queryset.annotate(in_price=Case(When(in_price=None, then=0),  default=F('in_price'), output_field=IntegerField())) \
                           .annotate(out_price=Case(When(out_price=None, then=0), default=F('out_price'), output_field=IntegerField()))

        total = queryset.count()

        if releaseTypeFilter != '전체':
            queryset = queryset.filter(type=releaseTypeFilter)

        if productTypeFilter:
            queryset = queryset.filter(code=productTypeFilter)

        if locatoinTypeFilter:
            queryset = queryset.filter(Q(in_locationCode__code=locatoinTypeFilter) |
                                       Q(locationCode__code=locatoinTypeFilter))

        if order == 'desc':
            order_column = '-' + order_column

        if search_value:
            queryset = queryset.filter(Q(memo__icontains=search_value) | Q(locationCodeName__icontains=search_value))

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
    def eggReportQuery(**kwargs):
        ORDER_COLUMN_CHOICES = Choices(
            ('0', 'codeName'),
            ('1', 'in_ymd'),
            ('2', 'in_locationCodeName'),
            ('3', 'previousStock'),
            ('4', 'in'),
            ('5', 'in_price'),
            ('6', 'sale'),
            ('7', 'sale_price'),
            ('8', 'loss'),
            ('9', 'insert'),
            ('10', 'release'),
            ('11', 'currentStock')
        )
        draw = int(kwargs.get('draw', None)[0])
        search_value = kwargs.get('search[value]', None)[0]
        order_column = kwargs.get('order[0][column]', None)[0]
        order = kwargs.get('order[0][dir]', None)[0]
        order_column = ORDER_COLUMN_CHOICES[order_column]
        start_date = kwargs.get('start_date', None)[0]
        end_date = kwargs.get('end_date', None)[0]
        arr = []

        egg_previous = Egg.objects.values('code', 'codeName', 'in_ymd', 'in_locationCodeName') \
            .annotate(totalCount=Sum('count')) \
            .filter(ymd__lt=start_date) \
            .filter(totalCount__gt=0)  # 재고가 0초과인 이전 재고

        if search_value:
            egg_previous = egg_previous.filter(Q(codeName__icontains=search_value) |
                                               Q(in_locationCodeName__icontains=search_value))
        for previous in egg_previous:  # 기간 내 전일재고의 각 타입별(IN, SALE, LOSS, INSERT) count를 구한다
            result = {}
            countPerType = Egg.objects.values('code', 'codeName', 'in_ymd', 'in_locationCodeName', 'type') \
                .annotate(totalCount=Sum('count')) \
                .annotate(totalPrice=Sum('price')) \
                .filter(code=previous['code']) \
                .filter(in_ymd=previous['in_ymd']) \
                .filter(in_locationCodeName=previous['in_locationCodeName']) \
                .filter(ymd__gte=start_date) \
                .filter(ymd__lte=end_date)
            PREVIOUS_STOCK = previous["totalCount"]
            # IN = 0
            SALE = 0
            SALE_PRICE = 0
            LOSS = 0
            INSERT = 0
            for element in countPerType:  # 전일재고니깐 생성 없음
                number = element["totalCount"]
                price = element["totalPrice"]
                if element['type'] == '판매':
                    SALE += number
                    if price:
                        SALE_PRICE += price
                elif element['type'] == '폐기':
                    LOSS += number
                elif element['type'] == '생산':
                    INSERT += number
            RELEASE = SALE + LOSS + INSERT
            CURRENT_STOCK = PREVIOUS_STOCK + RELEASE
            if SALE == 0: SALE = None
            if SALE_PRICE == 0: SALE_PRICE = None
            if LOSS == 0: LOSS = None
            if INSERT == 0: INSERT = None
            if RELEASE == 0: RELEASE = None
            # if CURRENT_STOCK == 0: CURRENT_STOCK = None
            result['codeName'] = previous['codeName']
            result['in_ymd'] = previous['in_ymd']
            result['in_locationCodeName'] = previous['in_locationCodeName']
            result['previousStock'] = PREVIOUS_STOCK
            result['in'] = None
            result['in_price'] = None
            result['sale'] = SALE
            result['sale_price'] = SALE_PRICE
            result['loss'] = LOSS
            result['insert'] = INSERT
            result['release'] = RELEASE
            result['currentStock'] = CURRENT_STOCK
            arr.append(result)

        # 기간 내 생산되고 출고된 것들의 현재고 구하기(전일재고 당연히 없음)
        egg_period = Egg.objects.values('code', 'codeName', 'in_ymd', 'in_locationCodeName') \
            .annotate(totalCount=Sum('count')) \
            .filter(ymd__gte=start_date) \
            .filter(ymd__lte=end_date) \
            .filter(type='입고')

        if search_value:
            egg_period = egg_period.filter(Q(codeName__icontains=search_value) |
                                               Q(in_locationCodeName__icontains=search_value))

        for period in egg_period:  # 기간 내 생성된 각 타입별(IN, SALE, LOSS, INSERT) count를 구한다
            result = {}
            countPerType = Egg.objects.values('code', 'codeName', 'in_ymd', 'in_locationCodeName', 'type') \
                .annotate(totalCount=Sum('count')) \
                .annotate(totalPrice=Sum('price')) \
                .filter(code=period['code']) \
                .filter(in_ymd=period['in_ymd']) \
                .filter(in_locationCodeName=period['in_locationCodeName']) \
                .filter(ymd__gte=start_date) \
                .filter(ymd__lte=end_date)
            IN = 0
            SALE = 0
            IN_PRICE = 0
            SALE_PRICE = 0
            LOSS = 0
            INSERT = 0
            for element in countPerType:  # 전일재고니깐 생성 없음
                number = element["totalCount"]
                price = element["totalPrice"]
                if element['type'] == '판매':
                    SALE += number
                    if price:
                        SALE_PRICE += price
                elif element['type'] == '폐기':
                    LOSS += number
                elif element['type'] == '생산':
                    INSERT += number
                elif element['type'] == '입고':
                    IN += number
                    if price:
                        IN_PRICE += price
            RELEASE = SALE + LOSS + INSERT
            CURRENT_STOCK = IN + RELEASE
            if SALE == 0: SALE = None
            if SALE_PRICE == 0: SALE_PRICE = None
            if IN == 0: IN = None
            if IN_PRICE == 0: IN_PRICE = None
            if LOSS == 0: LOSS = None
            if INSERT == 0: INSERT = None
            if RELEASE == 0: RELEASE = None
            result['codeName'] = period['codeName']
            result['in_ymd'] = period['in_ymd']
            result['in_locationCodeName'] = period['in_locationCodeName']
            result['previousStock'] = None
            result['in'] = IN
            result['in_price'] = IN_PRICE
            result['sale'] = SALE
            result['sale_price'] = SALE_PRICE
            result['loss'] = LOSS
            result['insert'] = INSERT
            result['release'] = RELEASE
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

    @staticmethod
    def getAmount(start_date, end_date):
        return Egg.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date).filter(type__in=['입고', '생산']) \
            .aggregate(totalAmount=Sum('amount'))['totalAmount']
