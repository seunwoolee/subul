from datetime import datetime
from operator import itemgetter, attrgetter

from django.db import models
from django.db.models import Q, Sum, F, ExpressionWrapper, FloatField, DecimalField, Value, IntegerField, Func, \
    CharField
from model_utils import Choices
from itertools import chain

from eggs.models import Egg
from product.models import ProductCode
from core.models import Master, Detail, Location
from release.models import Release


class ABS(Func):
    function = 'ABS'


class Order(Detail):
    ORDER_TYPE_CHOICES = (
        ('판매', '판매'),
        ('샘플', '샘플'),
        ('증정', '증정'),
        ('자손', '자손'),
        ('생산요청', '생산요청'),
    )

    SPECIALTAG_TYPE_CHOICES = (
        ('', '일반'),
        ('특인가', '특인가'),
    )
    productCode = models.ForeignKey(ProductCode, on_delete=models.CASCADE, null=True, blank=True)
    orderLocationCode = models.ForeignKey(Location, on_delete=models.CASCADE)
    orderLocationName = models.CharField(max_length=255)
    type = models.CharField(
        max_length=10,
        choices=ORDER_TYPE_CHOICES,
        default='판매',
    )
    price = models.DecimalField(decimal_places=1, max_digits=19)
    setProduct = models.ForeignKey('product.SetProductCode', on_delete=models.CASCADE, null=True, blank=True)
    release_id = models.ForeignKey('release.Release', on_delete=models.SET_NULL, null=True, blank=True)
    specialTag = models.CharField(
        max_length=10,
        choices=SPECIALTAG_TYPE_CHOICES,
        default='',
        blank=True
    )

    def __str__(self):
        return f"{self.ymd}_{self.orderLocationName}_{self.codeName}"

    @staticmethod
    def orderQuery(**kwargs):
        draw = int(kwargs.get('draw', None)[0])
        start = int(kwargs.get('start', None)[0])
        length = int(kwargs.get('length', None)[0])
        search_value = kwargs.get('search[value]', None)[0]
        start_date = kwargs.get('start_date', None)[0]
        end_date = kwargs.get('end_date', None)[0]
        order_column = kwargs.get('order[0][column]', None)[0]
        order = kwargs.get('order[0][dir]', None)[0]
        releaseOrder = kwargs.get("releaseOrder", None)
        user_instance = kwargs.get("user_instance", None)[0]
        checkBoxFilter = kwargs.get('checkBoxFilter', [''])[0]
        location_manager = kwargs.get('location_manager', [''])[0]
        gubunFilter = kwargs.get('gubunFilter', [''])[0]

        if checkBoxFilter: checkBoxFilter = checkBoxFilter.split(',')

        if not releaseOrder:  # 주문내역조회
            if gubunFilter == "stepOne":
                ORDER_COLUMN_CHOICES = Choices(
                    ('0', 'id'),
                    ('1', 'type'),
                    ('2', 'specialTag'),
                    ('3', 'ymd'),
                    ('4', 'orderLocationName'),
                    ('5', 'codeName'),
                    ('6', 'amount'),
                    ('7', 'count'),
                    ('8', 'price'),
                    ('9', 'totalPrice'),
                    ('10', 'memo'),
                    ('11', 'setProduct'),
                )
                order_column = ORDER_COLUMN_CHOICES[order_column]
                queryset = Order.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date) \
                    .filter(delete_state='N').annotate(totalPrice=Sum(F('count') * F('price'), output_field=IntegerField())) \
                    .annotate(setProductCode=F('setProduct__code'))

                total = queryset.count()

                if search_value:
                    queryset = queryset.filter(Q(orderLocationName__icontains=search_value) |
                                               Q(codeName__icontains=search_value) |
                                               Q(memo__icontains=search_value))

            elif gubunFilter == 'stepTwo':
                ORDER_COLUMN_CHOICES = Choices(
                    ('0', 'id'),
                    ('1', 'type'),
                    ('2', 'specialTag'),
                    ('3', 'ymd'),
                    ('4', 'orderLocationName'),
                    ('5', 'codeName'),
                    ('6', 'amount'),
                    ('7', 'count'),
                    ('8', 'release_ymd'),
                    ('9', 'release_type'),
                    ('10', 'release_locationName'),
                    ('11', 'release_codeName'),
                    ('12', 'release_amount'),
                    ('13', 'release_count'),
                    ('14', 'release_price'),
                )
                order_column = ORDER_COLUMN_CHOICES[order_column]
                queryset = Order.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date).filter(delete_state='N') \
                    .annotate(release_ymd=F('release_id__ymd')) \
                    .annotate(release_type=F('release_id__type')) \
                    .annotate(release_locationName=F('release_id__releaseLocationName')) \
                    .annotate(release_codeName=F('release_id__codeName')) \
                    .annotate(release_amount=F('release_id__amount')) \
                    .annotate(release_count=F('release_id__count')) \
                    .annotate(release_price=F('release_id__price'))
                total = queryset.count()
                if search_value:
                    queryset = queryset.filter(Q(orderLocationName__icontains=search_value) |
                                               Q(codeName__icontains=search_value))
        else:  # 주문내역출고등록(출고)
            ORDER_COLUMN_CHOICES = Choices(
                ('0', 'id'),
                ('1', 'type'),
                ('2', 'specialTag'),
                ('3', 'ymd'),
                ('4', 'orderLocationName'),
                ('5', 'codeName'),
                ('6', 'amount'),
                ('7', 'count'),
                ('8', 'memo'),
            )
            order_column = ORDER_COLUMN_CHOICES[order_column]
            queryset = Order.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date) \
                .filter(delete_state='N').annotate(totalPrice=Sum(F('count') * F('price'), output_field=IntegerField())) \
                .annotate(setProductCode=F('setProduct__code'))
            total = queryset.count()
            if search_value:  #
                queryset = queryset.filter(Q(orderLocationName__icontains=search_value) |
                                           Q(codeName__icontains=search_value) |
                                           Q(memo__icontains=search_value))

        if order == 'desc':
            order_column = '-' + order_column

        count = queryset.count()

        if not releaseOrder:
            if checkBoxFilter:
                queryset = queryset.filter(orderLocationCode__location_character__in=checkBoxFilter)
                count = queryset.count()

            if location_manager == "true":
                queryset = queryset.filter(orderLocationCode__location_manager=user_instance)
                count = queryset.count()
        else:
            queryset = queryset.filter(release_id=None).order_by(order_column)  # 출고가능한 ORDER

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
    def orderStepThreeQuery(**kwargs):
        draw = int(kwargs.get('draw', None)[0])
        start = int(kwargs.get('start', None)[0])
        length = int(kwargs.get('length', None)[0])
        search_value = kwargs.get('search[value]', None)[0]
        start_date = kwargs.get('start_date', None)[0]
        end_date = kwargs.get('end_date', None)[0]
        order_column = kwargs.get('order[0][column]', None)[0]
        order = kwargs.get('order[0][dir]', None)[0]
        mergedProductInfo = {}
        ORDER_COLUMN_CHOICES = {
            '0': 'id',
            '1': 'ymd',
            '2': 'releaseLocationName',
            '3': 'code',
            '4': 'codeName',
            '5': 'count',
            '6': 'amount',
            '7': 'price',
            '8': 'supplyPrice',
            '9': 'releaseVat'
        }
        order_column = ORDER_COLUMN_CHOICES[order_column]
        queryset_release = Release.objects.values('id', 'ymd', 'releaseLocationName', 'code', 'codeName', 'count',
                                                  'amount', 'price', 'releaseVat') \
            .filter(ymd__gte=start_date) \
            .filter(ymd__lte=end_date).filter(type='판매') \
            .annotate(supplyPrice=ExpressionWrapper(F('price') - F('releaseVat'), output_field=DecimalField()))
        queryset_egg = Egg.objects.values('id', 'ymd', 'code', 'codeName', 'amount', 'price') \
            .filter(ymd__gte=start_date).filter(ymd__lte=end_date).filter(type='판매') \
            .annotate(count=ABS(F('count'))) \
            .annotate(releaseLocationName=F('locationCodeName')).annotate(releaseVat=Value(0, IntegerField())) \
            .annotate(supplyPrice=F('price'))
        mergedProductInfo['recordsTotal'] = queryset_release.count() + queryset_egg.count()
        if search_value:
            queryset_release = queryset_release.filter(Q(releaseLocationName__icontains=search_value) |
                                                       Q(codeName__icontains=search_value))
            queryset_egg = queryset_egg.filter(Q(locationCodeName__icontains=search_value) |
                                               Q(codeName__icontains=search_value))
        mergedProductInfo['recordsFiltered'] = queryset_release.count() + queryset_egg.count()
        mergedProductInfo['data'] = list(chain(queryset_release, queryset_egg))
        if order == 'desc':
            mergedProductInfo['data'] = sorted(mergedProductInfo['data'],
                                               key=lambda k: k[order_column] if k[order_column] is not None
                                               else 0, reverse=True)
        else:
            mergedProductInfo['data'] = sorted(mergedProductInfo['data'],
                                               key=lambda k: k[order_column] if k[order_column] is not None
                                               else 0)
        mergedProductInfo['data'] = mergedProductInfo['data'][start:start + length]  # 페이징
        mergedProductInfo['draw'] = draw
        return mergedProductInfo