from django.db import models
from django.db.models import Q, Sum, F
from model_utils import Choices
from product.models import ProductCode
from core.models import Master, Detail, Location


# class OrderMaster(Master):
#     pass


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
    price = models.IntegerField()
    setProduct = models.ForeignKey('product.SetProductCode', on_delete=models.CASCADE, null=True, blank=True)
    release_id = models.ForeignKey('release.Release', on_delete=models.CASCADE, null=True, blank=True)
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
        checkBoxFilter = None
        gubunFilter = None
        if length != -1:
            checkBoxFilter = kwargs.get('checkBoxFilter', None)[0]
            gubunFilter = kwargs.get('gubunFilter', None)[0]
        if checkBoxFilter: checkBoxFilter = checkBoxFilter.split(',')

        if length != -1:  # 주문내역조회
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
                    .filter(delete_state='N').annotate(totalPrice=Sum(F('count') * F('price'))) \
                    .annotate(setProductCode=F('setProduct__code'))

                total = queryset.count()
                if search_value:  #
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
                queryset = Order.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date).filter(delete_state='N')\
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
                .filter(delete_state='N').annotate(totalPrice=Sum(F('count') * F('price'))) \
                .annotate(setProductCode=F('setProduct__code'))
            total = queryset.count()
            if search_value:  #
                queryset = queryset.filter(Q(orderLocationName__icontains=search_value) |
                                           Q(codeName__icontains=search_value) |
                                           Q(memo__icontains=search_value))
        # django orm '-' -> desc
        if order == 'desc':
            order_column = '-' + order_column

        # total = queryset.count()
        # if search_value:
        #     queryset = queryset.filter(Q(orderLocationName__icontains=search_value) |
        #                                Q(codeName__icontains=search_value) |
        #                                Q(memo__icontains=search_value))
        count = queryset.count()

        if length != -1:
            if checkBoxFilter:  # TODO 담당자 검색
                queryset = queryset.filter(orderLocationCode__type__in=checkBoxFilter)

            queryset = queryset.order_by(order_column)[start:start + length]
        else:
            queryset = queryset.filter(release_id=None).order_by(order_column)  # 출고가능한 ORDER

        return {
            'items': queryset,
            'count': count,
            'total': total,
            'draw': draw
        }
