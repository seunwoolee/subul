from django.db import models
from core.models import Master, Detail, Location

class ReleaseMaster(Master):
    price = models.IntegerField()


class Release(Detail):
    RELEASE_TYPE_CHOICES = (
        ('판매', '판매'),
        ('샘플', '샘플'),
        ('증정', '증정'),
        ('자손', '자손'),
    )

    master_id = models.ForeignKey(ReleaseMaster,
                                  on_delete=models.CASCADE,
                                  related_name='master_id')
    type = models.CharField(
        max_length=10,
        choices=RELEASE_TYPE_CHOICES,
        default='판매',
    )
    product_id = models.ForeignKey('product.ProductAdmin', on_delete=models.CASCADE,related_name='product', default='')
    productYmd = models.CharField(max_length=8)
    releaseLocationCode = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='release_locationCode')
    releaseLocationName = models.CharField(max_length=255)
    price = models.IntegerField()
    releaseOrder = models.ForeignKey('order.Order', on_delete=models.CASCADE)
    releaseStoreLocation = models.CharField(max_length=255)  # TODO 포링키 고민
    releaseSetProductCode = models.ForeignKey('product.SetProductCode', on_delete=models.CASCADE)
    releaseVat = models.IntegerField()
