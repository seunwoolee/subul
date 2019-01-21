from django.db import models
from django.db.models import SET_DEFAULT
from users.models import CustomUser

DELETE_STATE_CHOICES = (
    ('Y', 'deleted'),
    ('N', 'notDeleted'),
)


class TimeStampedModel(models.Model):
    """
    created , modified filed를 제공해주는 abstract base class model임
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    delete_state = models.CharField(
        max_length=2,
        choices=DELETE_STATE_CHOICES,
        default='N',
    )

    class Meta:
        abstract = True


class Code(models.Model):
    code = models.CharField(max_length=255)
    codeName = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    delete_state = models.CharField(
        max_length=2,
        choices=DELETE_STATE_CHOICES,
        default='N',
    )

    class Meta:
        abstract = True


class Master(models.Model):
    ymd = models.CharField(max_length=8)
    totalCount = models.IntegerField(default=0)
    totalAmount = models.FloatField(default=0)
    delete_state = models.CharField(
        max_length=2,
        choices=DELETE_STATE_CHOICES,
        default='N',
    )

    class Meta:
        abstract = True


class Detail(models.Model):
    ymd = models.CharField(max_length=8)
    code = models.CharField(max_length=255)
    codeName = models.CharField(max_length=255)
    count = models.IntegerField()
    amount = models.FloatField()
    amount_kg = models.FloatField(blank=True, null=True)
    memo = models.TextField(blank=True, null=True)
    delete_state = models.CharField(
        max_length=2,
        choices=DELETE_STATE_CHOICES,
        default='N',
    )

    class Meta:
        abstract = True


class Out(models.Model):
    ymd = models.CharField(max_length=8)
    count = models.IntegerField()
    type = models.CharField(max_length=255)
    delete_state = models.CharField(
        max_length=2,
        choices=DELETE_STATE_CHOICES,
        default='N',
    )

    class Meta:
        abstract = True


class Location(Code):
    LOCATION_TYPE_CHOICES = (
        ('01', '포장재입고'),
        ('03', '원란입고'),
        ('05', '판매'),
        ('07', '원란판매'),
        ('09', 'OEM입고거래처'),
    )

    SHOPPINGMALL_TYPE_CHOICES = (
        ('Y', '쇼핑몰'),
        ('2', '보관장소'),
        ('N', '기본장소'),
    )

    CHARACTER_TYPE_CHOICES = (
        ('01', 'B2B'),
        ('02', '급식'),
        ('03', '미군납'),
        ('04', '백화점'),
        ('05', '온라인'),
        ('06', '자사몰'),
        ('07', '직거래'),
        ('08', '특판'),
        ('09', '하이퍼'),
        ('99', '기타'),
    )
    type = models.CharField(
        max_length=2,
        choices=LOCATION_TYPE_CHOICES,
        default='05',
    )
    location_address = models.CharField(max_length=255, blank=True, null=True)
    location_phone = models.CharField(max_length=255, blank=True, null=True)
    location_companyNumber = models.CharField(max_length=255, blank=True, null=True)
    location_owner = models.CharField(max_length=255, blank=True, null=True)
    location_shoppingmall = models.CharField(
        max_length=2,
        choices=SHOPPINGMALL_TYPE_CHOICES,
        default='N',
    )
    location_character = models.CharField(
        max_length=2,
        choices=CHARACTER_TYPE_CHOICES,
        default='99',
    )
    location_manager = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,  # TODO 담당자
                                         related_name='location_manager')

    def __str__(self):
        return self.codeName
