from django.db import models
from core.models import Detail, Location, Code


class PackingCode(Code):
    PACKING_TYPE_CHOICES = (
        ('포장재', '포장재'),
        ('외포장재', '외포장재'),
    )

    type = models.CharField(max_length=255, choices=PACKING_TYPE_CHOICES)
    size = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.codeName + '(' + self.code + ')'


class Packing(Detail):
    PACKING_TYPE_CHOICES = (
        ('입고', '입고'),
        ('생산', '생산'),
        ('폐기', '폐기'),
        ('조정', '조정'),
    )
    type = models.CharField(
        max_length=10,
        choices=PACKING_TYPE_CHOICES,
        default="입고"
    )
    price = models.IntegerField()
    locationCode = models.ForeignKey(Location, on_delete=models.CASCADE , null=True, blank=True)
    locationCodeName = models.CharField(max_length=255 , null=True, blank=True)
    packingCode = models.ForeignKey(PackingCode, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.codeName + '(' + self.ymd + ') ' + self.type