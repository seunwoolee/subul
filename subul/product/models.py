from django.db import models
from model_utils import Choices

from core.models import Code, Detail, Location, Out, TimeStampedModel
from release.models import Release
from django.db.models import Sum, Q, F
import datetime

DELETE_STATE_CHOICES = (
    ('Y', 'deleted'),
    ('N', 'notDeleted'),
)


class ProductMaster(models.Model):
    produce_id = models.IntegerField(default=0)
    ymd = models.CharField(max_length=8)
    total_loss_openEgg = models.FloatField(default=0)
    total_loss_insert = models.FloatField(default=0)
    total_loss_clean = models.FloatField(default=0)
    total_loss_fill = models.FloatField(default=0)
    total_openEgg = models.FloatField(default=0)
    total_eggUse = models.FloatField(default=0)
    total_storeInsert = models.FloatField(default=0)
    total_produceStore = models.FloatField(default=0)
    total_productAmount = models.FloatField(default=0)
    total_productCount = models.IntegerField(default=0)
    delete_state = models.CharField(
        max_length=2,
        choices=DELETE_STATE_CHOICES,
        default='N',
    )

    def __str__(self):
        return self.ymd + '_생산마스터'


class ProductEgg(models.Model):
    EGG_TYPE_CHOICES = (
        ('할란', '할란'),
        ('할란사용', '할란사용'),
        ('공정품투입', '공정품투입'),
        ('공정품발생', '공정품발생'),
    )

    TANK_TYPE_CHOICES = (
        ('01201', 'RAW Tank 전란'),
        ('01202', 'RAW Tank 난황'),
        ('01203', 'RAW Tank 난백'),
        ('01204', 'Past Tank 전란'),
        ('01205', 'Past Tank 난황'),
        ('01206', 'Past Tank 난백'),
        ('01207', 'RAW Tank 등급란 전란'),
        ('01208', 'RAW Tank 등급란 난황'),
        ('01209', 'RAW Tank 등급란 난백'),
    )

    CODE_TYPE_CHOICES = {
        '01201': 'RAW Tank 전란',
        '01202': 'RAW Tank 난황',
        '01203': 'RAW Tank 난백',
        '01204': 'Past Tank 전란',
        '01205': 'Past Tank 난황',
        '01206': 'Past Tank 난백',
        '01207': 'RAW Tank 등급란 전란',
        '01208': 'RAW Tank 등급란 난황',
        '01209': 'RAW Tank 등급란 난백'
    }

    master_id = models.ForeignKey(ProductMaster,
                                  on_delete=models.CASCADE,
                                  related_name='temp')
    ymd = models.CharField(max_length=8)
    type = models.CharField(
        max_length=30,
        choices=EGG_TYPE_CHOICES,
        default='',
    )
    code = models.CharField(max_length=10, default='01201')
    codeName = models.CharField(max_length=255, default=CODE_TYPE_CHOICES['01201'])
    rawTank_amount = models.FloatField(default=0)
    pastTank_amount = models.FloatField(default=0)
    loss_insert = models.FloatField(default=0)
    loss_openEgg = models.FloatField(default=0)
    memo = models.TextField(blank=True)
    delete_state = models.CharField(
        max_length=2,
        choices=DELETE_STATE_CHOICES,
        default='N',
    )

    def __str__(self):
        return self.type + '_' + self.codeName + '(' + self.ymd + ')'

    @staticmethod
    def makeVaildinfo(productEggInfo, memo):  # ('이름','실제값') -> ('이름','실제값','메모')
        # print(productEggInfo, memo)
        j = 0
        for info in productEggInfo:  # ('이름','실제값','메모')
            if '메모' in info[0]:
                j += 1
                pass
            else:
                info.append(memo[j])

        return productEggInfo

    @staticmethod
    def insertInfo(main, validInfo):
        for info in validInfo:  # ('이름','실제값','메모')
            if info[1] and '메모' not in info[0]:  # 값이 있으며 AND 메모가 아닌경우
                type, rawOrPastType, code = info[0].split("_")
                productEgg = ProductEgg.objects.create(
                    master_id=main,
                    ymd=main.ymd,
                    type=type,
                    code=code,
                    codeName=ProductEgg.CODE_TYPE_CHOICES[code],
                    memo=info[2],
                )

                if '투입' in type or '사용' in type:  # 공정품투입 , 할란사용 경우 -number 입력
                    info[1] = -info[1]

                if 'RawTank' in rawOrPastType:
                    productEgg.rawTank_amount = info[1]
                elif 'PastTank' in rawOrPastType:
                    productEgg.pastTank_amount = info[1]
                productEgg.save()  # TODO 할란 , 할란사용 수율 비례식 계산 필요

    @staticmethod
    def getLossOpenEggPercent(masterInstance):
        total_rawTank_amount = 0
        eggs = ProductEgg.objects.filter(master_id=masterInstance).filter(type='할란').filter(delete_state='N')
        for egg in eggs:
            total_rawTank_amount += egg.rawTank_amount

        try:
            for egg in eggs:
                percent = egg.rawTank_amount / total_rawTank_amount
                print(egg.rawTank_amount, percent, total_rawTank_amount, masterInstance.total_loss_openEgg)
                openEgglossPercent = round(masterInstance.total_loss_openEgg * percent, 2)
                insertlossPercent = round(masterInstance.total_loss_insert * percent, 2)
                egg.loss_openEgg = openEgglossPercent
                egg.loss_insert = insertlossPercent
                egg.save()
        except ZeroDivisionError:
            pass


class ProductCode(Code):
    CONTENT_TYPE_CHOICES = (
        ('전란', '전란'),
        ('난백', '난백'),
        ('난황', '난황'),
        ('X', '없음'),
    )

    STORE_TYPE_CHOICES = (
        ('AP', 'AP'),
        ('BIB', 'BIB'),
        ('CT', 'CT'),
        ('PAC', 'PAC'),
        ('PKG', 'PKG'),
        ('TANK', 'TANK'),
        ('TON', 'TON'),
        ('TOTE', 'TOTE'),
        ('', '없음'),
    )

    type = models.CharField(
        max_length=10,
        choices=CONTENT_TYPE_CHOICES,
        default='',
    )

    amount_kg = models.FloatField()
    price = models.IntegerField()
    store_type = models.CharField(
        max_length=10,
        choices=STORE_TYPE_CHOICES,
        default=''
    )
    vat = models.IntegerField(default=0)
    expiration = models.IntegerField(default=0)

    def __str__(self):
        return self.codeName + '(' + self.code + ')'


class Product(Detail):  # TODO 주문 나갈때 Tag 붙이는 필드 필요
    master_id = models.ForeignKey(ProductMaster,
                                  on_delete=models.CASCADE,
                                  related_name='master_id')
    loss_clean = models.FloatField(default=0)
    loss_fill = models.FloatField(default=0)
    '''OEM 상품에 한해서 있는 필드'''
    purchaseYmd = models.CharField(max_length=8, blank=True, null=True)
    purchaseLocation = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='purchase_locationCode',
                                         blank=True, null=True)
    purchaseLocationName = models.CharField(max_length=255, blank=True, null=True)
    productCode = models.ForeignKey(ProductCode, on_delete=models.CASCADE,
                                    blank=True, null=True, related_name='productInfo')

    def __str__(self):
        return self.codeName + '(' + self.ymd + ')'

    @staticmethod
    def getLossProductPercent(masterInstance):
        total_product_amount = 0
        products = Product.objects.filter(master_id=masterInstance).filter(delete_state='N')
        for product in products:
            total_product_amount += product.amount

        try:
            for product in products:
                percent = product.amount / total_product_amount
                cleanLossPercent = round(masterInstance.total_loss_clean * percent, 2)
                fillLossPercent = round(masterInstance.total_loss_fill * percent, 2)
                product.loss_clean = cleanLossPercent
                product.loss_fill = fillLossPercent
                product.save()
        except ZeroDivisionError:
            pass


class ProductAdmin(models.Model):
    RELEASE_TYPE_CHOICES = (
        ('생성', '생성'),
        ('판매', '판매'),
        ('샘플', '샘플'),
        ('증정', '증정'),
        ('자손', '자손'),
        ('이동', '이동'),
        ('반품', '반품'),  # TODO 반품 처리
    )
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.FloatField()
    count = models.IntegerField()
    ymd = models.CharField(max_length=8)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    releaseType = models.CharField(
        max_length=10,
        choices=RELEASE_TYPE_CHOICES,
        default='생성',
    )
    releaseSeq = models.ForeignKey(Release, on_delete=models.CASCADE, null=True, blank=True)
    delete_state = models.CharField(
        max_length=2,
        choices=DELETE_STATE_CHOICES,
        default='N',
    )

    def __str__(self):
        return self.product_id.codeName + '(' + self.ymd + ') _' + self.releaseType

    @staticmethod
    def productAdminQuery(**kwargs):

        ORDER_COLUMN_CHOICES = Choices(
            ('0', 'productCodeName'),
            ('1', 'productYmd'),
            ('2', 'storedLocationCodeName'),
            ('3', 'totalAmount'),
            ('4', 'totalCount'),
        )
        draw = int(kwargs.get('draw', None)[0])
        search_value = kwargs.get('search[value]', None)[0]
        order_column = kwargs.get('order[0][column]', None)[0]
        order = kwargs.get('order[0][dir]', None)[0]
        order_column = ORDER_COLUMN_CHOICES[order_column]

        queryset = ProductAdmin.objects.values(productId=F('product_id'),
                                               productCode=F('product_id__code'),
                                               productCodeName=F('product_id__codeName'),
                                               productYmd=F('ymd'),
                                               storedLocationCode=F('location__code'),
                                               amount_kg=F('product_id__amount_kg'),
                                               storedLocationCodeName=F('location__codeName')) \
            .annotate(totalCount=Sum('count')) \
            .annotate(totalAmount=Sum('amount')) \
            .filter(totalCount__gt=0)

        # django orm '-' -> desc
        if order == 'desc':
            order_column = '-' + order_column

        total = queryset.count() # TODO 삭제

        if search_value:
            queryset = queryset.filter(Q(productCodeName__icontains=search_value) |
                                       Q(productYmd__icontains=search_value) |
                                       Q(storedLocationCodeName__icontains=search_value))

        count = queryset.count() # TODO 삭제
        queryset = queryset.order_by(order_column)
        return {
            'items': queryset,
            'count': count,
            'total': total,
            'draw': draw
        }

    @staticmethod
    def productAdminOrderQuery(productCode, storedLocationCode):

        queryset = ProductAdmin.objects.values(productId=F('product_id'),
                                               productCode=F('product_id__code'),
                                               productCodeName=F('product_id__codeName'),
                                               productYmd=F('ymd'),
                                               storedLocationCode=F('location__code'),
                                               amount_kg=F('product_id__amount_kg'),
                                               storedLocationCodeName=F('location__codeName')) \
            .annotate(totalCount=Sum('count')) \
            .annotate(totalAmount=Sum('amount')) \
            .filter(storedLocationCode=storedLocationCode)\
            .filter(productCode=productCode)\
            .filter(totalCount__gt=0)\
            .order_by('productYmd')
        return queryset


class ProductUnitPrice(TimeStampedModel):
    locationCode = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location')
    productCode = models.ForeignKey(ProductCode, on_delete=models.CASCADE, related_name='product')
    price = models.IntegerField(default=0)


class SetProductCode(Code):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.codeName}_ {self.location.codeName}"


class SetProductMatch(TimeStampedModel):
    setProductCode = models.ForeignKey(SetProductCode, on_delete=models.CASCADE)
    productCode = models.ForeignKey(ProductCode, on_delete=models.CASCADE)
    price = models.IntegerField()
    count = models.IntegerField(blank=True, null=True)
    saleLocation = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.setProductCode.codeName}_{self.saleLocation.codeName}_{self.productCode.codeName}"

def productQuery(**kwargs):
    search_value = kwargs.get('search[value]', None)[0]
    start_date = kwargs.get('start_date', None)[0]
    end_date = kwargs.get('end_date', None)[0]
    queryset = Product.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date).filter(
        delete_state='N')  # TODO delete state Y -> N으로 수정
    total = queryset.count()

    if search_value:
        queryset = queryset.filter(Q(code__icontains=search_value) |
                                   Q(codeName__icontains=search_value) |
                                   Q(memo__icontains=search_value))

    count = queryset.count()
    return {
        'items': queryset,
        'count': count,
        'total': total
    }


def productEggQuery(**kwargs):
    search_value = kwargs.get('search[value]', None)[0]
    start_date = kwargs.get('start_date', None)[0]
    end_date = kwargs.get('end_date', None)[0]
    queryset = ProductEgg.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date).filter(delete_state='N')
    total = queryset.count()

    if search_value:
        queryset = queryset.filter(Q(code__icontains=search_value) |
                                   Q(codeName__icontains=search_value) |
                                   Q(memo__icontains=search_value))

    count = queryset.count()
    return {
        'items': queryset,
        'count': count,
        'total': total
    }
