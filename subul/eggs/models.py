from django.db import models
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
    price = models.IntegerField()
    locationCode = models.ForeignKey(Location, on_delete=models.CASCADE)
    locationCodeName = models.CharField(max_length=255)
    eggCode = models.ForeignKey(EggCode, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.codeName + '(' + self.ymd + ') ' + self.type