from django.db import models
from django.db.models import Q, Sum, F, ExpressionWrapper, DecimalField, Value, IntegerField, Func, \
    CharField
from model_utils import Choices

from product.models import ProductCode
from core.models import Detail, Location
from release.models import Release
from users.models import CustomUser


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
        locationFilter = kwargs.get('locationFilter', [''])[0]
        managerFilter = kwargs.get('managerFilter', [''])[0]
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
                    ('4', 'weekday'),
                    ('5', 'orderLocationName'),
                    ('6', 'codeName'),
                    ('7', 'amount'),
                    ('8', 'count'),
                    ('9', 'price'),
                    ('10', 'totalPrice'),
                    ('11', 'memo'),
                    ('12', 'setProduct'),
                )
                order_column = ORDER_COLUMN_CHOICES[order_column]
                queryset = Order.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date) \
                    .annotate(totalPrice=Sum(F('count') * F('price'), output_field=IntegerField())) \
                    .annotate(setProductCode=F('setProduct__code'))

                total = queryset.count()

                if locationFilter:
                    queryset = queryset.filter(orderLocationCode__code=locationFilter)

                if managerFilter:
                    queryset = queryset.filter(
                        orderLocationCode__location_manager=CustomUser.objects.get(username=managerFilter))

                if checkBoxFilter:
                    queryset = queryset.filter(orderLocationCode__location_character__in=checkBoxFilter)

                if location_manager == "true":
                    queryset = queryset.filter(orderLocationCode__location_manager=user_instance)

                if search_value:
                    queryset = queryset.filter(Q(codeName__icontains=search_value) |
                                               Q(memo__icontains=search_value))

            elif gubunFilter == 'stepTwo':
                ORDER_COLUMN_CHOICES = Choices(
                    ('0', 'order_id'),
                    ('1', 'order_type'),
                    ('2', 'order_specialTag'),
                    ('3', 'order_ymd'),
                    ('4', 'order_orderLocationName'),
                    ('5', 'order_codeName'),
                    ('6', 'order_amount'),
                    ('7', 'order_count'),
                    ('8', 'order_totalPrice'),
                    ('9', 'release_ymd'),
                    ('10', 'release_amount'),
                    ('11', 'release_count'),
                    ('12', 'release_totalPrice'),
                )
                order_column = ORDER_COLUMN_CHOICES[order_column]

                queryset0 = Order.objects.values(
                    order_id=F('id'),
                    order_type=F('type'),
                    order_specialTag=F('specialTag'),
                    order_ymd=F('ymd'),
                    order_orderLocationName=F('orderLocationName'),
                    order_codeName=F('codeName'),
                    order_amount=F('amount'),
                    order_count=F('count'))\
                    .filter(ymd__gte=start_date).filter(ymd__lte=end_date).filter(release_id=None)\
                    .annotate(order_totalPrice=ExpressionWrapper(F('count') * F('price'),
                                                                 output_field=IntegerField()))\
                    .annotate(release_ymd=Value('', output_field=CharField())) \
                    .annotate(release_amount=Value(0, output_field=DecimalField())) \
                    .annotate(release_count=Value(0, output_field=IntegerField())) \
                    .annotate(release_totalPrice=Value(0, output_field=IntegerField()))

                queryset = Release.objects.values(
                    order_id=F('releaseOrder__id'),
                    order_type=F('releaseOrder__type'),
                    order_specialTag=F('releaseOrder__specialTag'),
                    order_ymd=F('releaseOrder__ymd'),
                    order_orderLocationName=F('releaseOrder__orderLocationName'),
                    order_codeName=F('releaseOrder__codeName'),
                    order_amount=F('releaseOrder__amount'),
                    order_count=F('releaseOrder__count')) \
                    .filter(releaseOrder__ymd__gte=start_date) \
                    .filter(releaseOrder__ymd__lte=end_date) \
                    .annotate(order_totalPrice=ExpressionWrapper(F('releaseOrder__count') * F('releaseOrder__price'),
                                                                 output_field=IntegerField())) \
                    .annotate(release_ymd=F('ymd')) \
                    .annotate(release_amount=Sum('amount')) \
                    .annotate(release_count=Sum('count')) \
                    .annotate(release_totalPrice=Sum('price'))

                total = queryset0.count() + queryset.count()

                if locationFilter:
                    queryset0 = queryset0.filter(orderLocationCode__code=locationFilter)
                    queryset = queryset.filter(releaseOrder__orderLocationCode__code=locationFilter)

                if managerFilter:
                    queryset0 = queryset0.filter(orderLocationCode__location_manager=
                                                 CustomUser.objects.get(username=managerFilter))
                    queryset = queryset.filter(releaseOrder__orderLocationCode__location_manager=
                                               CustomUser.objects.get(username=managerFilter))

                if checkBoxFilter:
                    queryset0 = queryset0.filter(orderLocationCode__location_character__in=checkBoxFilter)
                    queryset = queryset.filter(releaseOrder__orderLocationCode__location_character__in=checkBoxFilter)

                if location_manager == "true":
                    queryset0 = queryset0.filter(orderLocationCode__location_manager=user_instance)
                    queryset = queryset.filter(releaseOrder__orderLocationCode__location_manager=user_instance)

                if search_value:
                    queryset0 = queryset0.filter(codeName__icontains=search_value)
                    queryset = queryset.filter(order_codeName__icontains=search_value)

                queryset = queryset.union(queryset0)

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
                .annotate(totalPrice=Sum(F('count') * F('price'), output_field=IntegerField())) \
                .annotate(setProductCode=F('setProduct__code'))

            total = queryset.count()

            if search_value:
                queryset = queryset.filter(Q(orderLocationName__icontains=search_value) |
                                           Q(codeName__icontains=search_value) |
                                           Q(memo__icontains=search_value))

        if order == 'desc':
            order_column = '-' + order_column

        if releaseOrder:
            queryset = queryset.filter(release_id=None)

        count = queryset.count()

        if releaseOrder:
            queryset = queryset.order_by('ymd', 'orderLocationName', order_column)
        else:
            queryset = queryset.order_by(order_column)

        return {
            'items': queryset,
            'count': count,
            'total': total,
            'draw': draw
        }
