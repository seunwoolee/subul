from django.db import models
from django.db.models import Sum, DecimalField, F, Q
from django.db.models.functions import Cast
from model_utils import Choices

from core.models import Detail, Location, Code


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

    amount = models.CharField(max_length=10, null=True, blank=True)

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
    def eggListQuery(**kwargs):

        ORDER_COLUMN_CHOICES = Choices(
            ('0', 'id'),
            ('1', 'type'),
            ('2', 'in_ymd'),
            ('3', 'codeName'),
            ('4', 'in_locationCodeName'),
            ('5', 'locationCodeName'),
            ('6', 'ymd'),
            ('7', 'count'),
            ('8', 'amount'),
            ('9', 'in_price'),
            ('10', 'out_price'),
            ('11', 'pricePerEa'),
            ('12', 'memo'),
        )
        draw = int(kwargs.get('draw', None)[0])
        search_value = kwargs.get('search[value]', None)[0]
        order_column = kwargs.get('order[0][column]', None)[0]
        order = kwargs.get('order[0][dir]', None)[0]
        order_column = ORDER_COLUMN_CHOICES[order_column]
        start_date = kwargs.get('start_date', None)[0]
        end_date = kwargs.get('end_date', None)[0]
        releaseTypeFilter = kwargs.get('releaseTypeFilter', None)[0]
        productTypeFilter = kwargs.get('productTypeFilter', None)[0]
        locatoinTypeFilter = kwargs.get('locatoinTypeFilter', None)[0]

        queryset = Egg.objects.all().filter(ymd__gte=start_date).filter(ymd__lte=end_date)
        total = queryset.count()

        if releaseTypeFilter != '전체':
            queryset = queryset.filter(type=releaseTypeFilter)

        if productTypeFilter:
            queryset = queryset.filter(code=productTypeFilter)

        if locatoinTypeFilter:
            queryset = queryset.filter(Q(in_locationCode__code=locatoinTypeFilter) |
                                       Q(locationCode__code=locatoinTypeFilter))

        # django orm '-' -> desc
        if order == 'desc':
            order_column = '-' + order_column

        if search_value:
            queryset = queryset.filter(Q(codeName__icontains=search_value))

        count = queryset.count()
        queryset = queryset.order_by(order_column)
        return {
            'items': queryset,
            'count': count,
            'total': total,
            'draw': draw
        }
