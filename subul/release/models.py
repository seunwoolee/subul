from django.db import models
from django.db.models import Q, F, ExpressionWrapper, FloatField
from model_utils import Choices

from core.models import Master, Detail, Location


class Release(Detail):
    RELEASE_TYPE_CHOICES = (
        ('판매', '판매'),
        ('샘플', '샘플'),
        ('증정', '증정'),
        ('자손', '자손'),
        ('반품', '반품'),
    )

    type = models.CharField(
        max_length=10,
        choices=RELEASE_TYPE_CHOICES,
        default='판매',
    )
    product_id = models.ForeignKey('product.Product', on_delete=models.CASCADE,related_name='product', null=True, blank=True)
    productYmd = models.CharField(max_length=8)
    releaseLocationCode = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='release_locationCode')
    releaseLocationName = models.CharField(max_length=255)
    price = models.IntegerField()
    releaseOrder = models.ForeignKey('order.Order', on_delete=models.CASCADE, null=True, blank=True)
    releaseStoreLocation = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='release_releaseStoreLocation')
    releaseSetProductCode = models.ForeignKey('product.SetProductCode', on_delete=models.CASCADE, null=True, blank=True)
    releaseVat = models.IntegerField()

    def __str__(self):
        return f"{self.codeName}_{self.type}_{self.releaseLocationName}"

    @staticmethod
    def releaseQuery(**kwargs):
        RELEASE_COLUMN_CHOICES = Choices(
            ('0', 'id'),
            ('1', 'ymd'),
            ('2', 'releaseLocationName'),
            ('3', 'contentType'),
            ('4', 'code'),
            ('5', 'codeName'),
            ('6', 'amount'),
            ('7', 'count'),
            ('8', 'kgPrice'),
            ('9', 'totalPrice'),
            ('10', 'supplyPrice'),
            ('11', 'releaseVat'),
            ('12', 'eaPrice'),
            ('13', 'productYmd'),
            ('14', 'type'),
            ('15', 'releaseStoreLocationCodeName'),
            ('16', 'orderMemo'),
            ('17', 'locationType'),
            ('18', 'locationManagerName'),
            ('19', 'releaseSetProduct'),
            ('20', 'releaseSetProductCodeName'),
        )
        draw = int(kwargs.get('draw', None)[0])
        start = int(kwargs.get('start', None)[0])
        length = int(kwargs.get('length', None)[0])
        search_value = kwargs.get('search[value]', None)[0]
        start_date = kwargs.get('start_date', None)[0]
        end_date = kwargs.get('end_date', None)[0]
        order_column = kwargs.get('order[0][column]', None)[0]
        order_column = RELEASE_COLUMN_CHOICES[order_column]
        order = kwargs.get('order[0][dir]', None)[0]

        queryset = Release.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date).filter(delete_state='N')\
                          .annotate(kgPrice=ExpressionWrapper(F('count')+F('amount'), output_field=FloatField())) \
                          .annotate(contentType=F('product_id__productCode__type'))\
                          .annotate(totalPrice=F('price')) \
                          .annotate(supplyPrice=ExpressionWrapper(F('price') + F('releaseVat'), output_field=FloatField()))\
                          .annotate(eaPrice=ExpressionWrapper(F('price') / F('count'), output_field=FloatField()))\
                          .annotate(releaseStoreLocationCodeName=F('releaseStoreLocation__codeName'))\
                          .annotate(orderMemo=F('releaseOrder__memo'))\
                          .annotate(locationType=F('releaseLocationCode__location_character'))\
                          .annotate(locationManagerName=F('releaseLocationCode__location_manager__first_name'))\
                          .annotate(releaseSetProduct=F('releaseSetProductCode__code'))\
                          .annotate(releaseSetProductCodeName=F('releaseSetProductCode__codeName'))
        total = queryset.count()

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