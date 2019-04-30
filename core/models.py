from django.db import models
from django.db.models import F, Q, When, Case, CharField, Value
from model_utils import Choices
from users.models import CustomUser


DELETE_STATE_CHOICES = (
    ('Y', 'deleted'),
    ('N', 'notDeleted'),
)


class TimeStampedModel(models.Model):
    """
    created , modified filed를 제공해주는 abstract base class model
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
    """
    ProductCode, EggCode 등 모든 코드 Model의 부모 클래스
    """

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


class Detail(models.Model):
    """
    Egg, Order, Packing, Product, Release의 부모 클래스
    """

    ymd = models.CharField(max_length=8)
    code = models.CharField(max_length=255)
    codeName = models.CharField(max_length=255)
    count = models.IntegerField()
    amount = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    amount_kg = models.DecimalField(decimal_places=2, max_digits=19, default=0, blank=True, null=True)
    memo = models.TextField(blank=True, null=True)

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
    location_manager = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name='location_manager')

    def __str__(self):
        return self.codeName

    @staticmethod
    def locationQuery(**kwargs) -> object:

        ORDER_COLUMN_CHOICES = Choices(
            ('0', 'id'),
            ('1', 'codeName'),
            ('2', 'location_owner'),
            ('3', 'location_phone'),
            ('4', 'location_companyNumber'),
            ('5', 'location_address'),
            ('6', 'character_string'),
            ('7', 'character_string'),
            ('8', 'location_manager_string'),
        )
        draw = int(kwargs.get('draw', None)[0])
        start = int(kwargs.get('start', None)[0])
        length = int(kwargs.get('length', None)[0])
        search_value = kwargs.get('search[value]', None)[0]
        order_column = kwargs.get('order[0][column]', None)[0]
        order = kwargs.get('order[0][dir]', None)[0]
        order_column = ORDER_COLUMN_CHOICES[order_column]
        type = kwargs.get('type', None)[0]

        queryset = Location.objects.all().filter(delete_state='N').filter(type=type)\
                    .annotate(type_string=Case(
                                    When(type='01', then=Value('포장재입고')),
                                    When(type='03', then=Value('원란입고')),
                                    When(type='07', then=Value('원란판매')),
                                    When(type='09', then=Value('OEM입고거래처')),
                                    default=Value('판매'),
                                    output_field=CharField()))\
                    .annotate(character_string=Case(
                                    When(location_character='01', then=Value('B2B')),
                                    When(location_character='02', then=Value('급식')),
                                    When(location_character='03', then=Value('미군납')),
                                    When(location_character='04', then=Value('백화점')),
                                    When(location_character='05', then=Value('온라인')),
                                    When(location_character='06', then=Value('자사몰')),
                                    When(location_character='07', then=Value('직거래')),
                                    When(location_character='08', then=Value('특판')),
                                    When(location_character='09', then=Value('하이퍼')),
                                    default=Value('기타'),
                                    output_field=CharField())) \
                    .annotate(location_manager_string=F('location_manager__first_name'))

        if order == 'desc':
            order_column = '-' + order_column

        total = queryset.count()

        if search_value:
            queryset = queryset.filter(codeName__icontains=search_value)

        count = queryset.count()
        queryset = queryset.order_by(order_column)[start:start + length]
        return {
            'items': queryset,
            'count': count,
            'total': total,
            'draw': draw
        }