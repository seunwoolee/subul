from django.db import models
from django.db.models import Q

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

    # def releaseQuery(**kwargs):
    #     search_value = kwargs.get('search[value]', None)[0]
    #     start_date = kwargs.get('start_date', None)[0]
    #     end_date = kwargs.get('end_date', None)[0]
    #     queryset = Release.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date).filter(delete_state='N')
    #     total = queryset.count()
    #
    #     if search_value:
    #         queryset = queryset.filter(Q(code__icontains=search_value) |
    #                                    Q(codeName__icontains=search_value) |
    #                                    Q(memo__icontains=search_value))
    #
    #     count = queryset.count()
    #     return {
    #         'items': queryset,
    #         'count': count,
    #         'total': total
    #     }
