from django.db import models
from core.models import Master, Detail, Location


class OrderMaster(Master):
    pass


class Order(Detail):
    ORDER_TYPE_CHOICES = (
        ('판매', '판매'),
        ('샘플', '샘플'),
        ('증정', '증정'),
        ('자손', '자손'),
        ('생산요청', '생산요청'),
    )
    master_id = models.ForeignKey(OrderMaster, on_delete=models.CASCADE)
    orderLocationCode = models.ForeignKey(Location, on_delete=models.CASCADE)
    orderLocationName = models.CharField(max_length=255)
    type = models.CharField(
        max_length=10,
        choices=ORDER_TYPE_CHOICES,
        default='판매',
    )
    price = models.IntegerField()
    setProduct = models.ForeignKey('product.SetProductCode',on_delete=models.CASCADE)
    release_id = models.ForeignKey('release.Release',on_delete=models.CASCADE)