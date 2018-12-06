from django.db import models
from django.db.models import Q, F, ExpressionWrapper, FloatField, Sum, DecimalField
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
        ('미출고품', '미출고품'),
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
            queryset = Release.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date).filter(delete_state='N') \
                .annotate(kgPrice=ExpressionWrapper(F('price') / F('amount'), output_field=FloatField())) \
                .annotate(contentType=F('product_id__productCode__type')) \
                .annotate(totalPrice=F('price')) \
                .annotate(supplyPrice=ExpressionWrapper(F('price') - F('releaseVat'), output_field=FloatField())) \
                .annotate(eaPrice=ExpressionWrapper(F('price') / F('count'), output_field=FloatField())) \
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
            queryset = Release.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date)\
                .filter(delete_state='N') \
                .values('code', 'codeName', 'type', 'specialTag') \
                .annotate(contentType=F('product_id__productCode__type')) \
                .annotate(amount=Sum('amount')) \
                .annotate(count=Sum('count')) \
                .annotate(totalPrice=Sum('price')) \
                .annotate(kgPrice=Cast(F('totalPrice') / F('amount'), DecimalField(max_digits=20, decimal_places=2))) \
                .annotate(supplyPrice=ExpressionWrapper(F('totalPrice') - F('releaseVat'), output_field=FloatField())) \
                .annotate(releaseVat=F('releaseVat')) \
                .annotate(eaPrice=ExpressionWrapper(F('totalPrice') / F('count'), output_field=FloatField())) \
                .annotate(releaseStoreLocationCodeName=F('releaseStoreLocation__codeName'))
        elif groupByFilter == 'stepThree':
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
            queryset = Release.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date).filter(delete_state='N') \
                .values('code', 'codeName', 'type', 'specialTag') \
                .annotate(contentType=F('product_id__productCode__type')) \
                .annotate(releaseLocationName=F('releaseLocationName')) \
                .annotate(amount=Sum('amount')) \
                .annotate(count=Sum('count')) \
                .annotate(totalPrice=Sum('price')) \
                .annotate(kgPrice=ExpressionWrapper(F('totalPrice') / F('amount'), output_field=FloatField())) \
                .annotate(supplyPrice=ExpressionWrapper(F('totalPrice') - F('releaseVat'), output_field=FloatField())) \
                .annotate(releaseVat=F('releaseVat')) \
                .annotate(eaPrice=ExpressionWrapper(F('totalPrice') / F('count'), output_field=FloatField())) \
                .annotate(releaseStoreLocationCodeName=F('releaseStoreLocation__codeName'))
        elif groupByFilter == 'stepFour':
            RELEASE_COLUMN_CHOICES = Choices(
                ('0', 'code'),
                ('1', 'codeName'),
                ('2', "type"),
                ('3', 'contentType'),
                ('4', 'amount'),
                ('5', 'count'),
                ('6', 'totalPrice'),
                ('7', 'kgPrice'),
                ('8', 'supplyPrice'),
                ('9', 'releaseVat'),
                ('10', "eaPrice"),
                ('11', "releaseStoreLocationCodeName")
            )
            order_column = RELEASE_COLUMN_CHOICES[order_column]
            queryset = Release.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date).filter(
                delete_state='N') \
                .values('releaseLocationName') \
                .annotate(amount=Sum('amount')) \
                .annotate(count=Sum('count')) \
                .annotate(totalPrice=Sum('price')) \
                .annotate(supplyPrice=ExpressionWrapper(F('totalPrice') - F('releaseVat'), output_field=FloatField())) \
                .annotate(releaseVat=F('releaseVat'))

        total = queryset.count()

        if releaseTypeFilter != '전체':
            queryset = queryset.filter(type=releaseTypeFilter)

        if productTypeFilter != '전체':
            queryset = queryset.filter(product_id__productCode__type=productTypeFilter)

        if checkBoxFilter:
            queryset = queryset.filter(releaseLocationCode__type__in=checkBoxFilter)

        if order == 'desc':
            order_column = '-' + order_column

        if search_value:
            queryset = queryset.filter(Q(code__icontains=search_value) |
                                       Q(codeName__icontains=search_value) |
                                       Q(memo__icontains=search_value))

        count = queryset.count()
        queryset = queryset.order_by(order_column)[start:start + length]
        return {
            'items': queryset,
            'count': count,
            'total': total,
            'draw': draw
        }
