from django.db import models
from django.db.models.functions import Cast
from django.http import QueryDict
from model_utils import Choices

from core.models import Code, Detail, Location, TimeStampedModel
from eggs.models import Egg
from release.models import Release
from django.db.models import Sum, Q, F, DecimalField, Value, IntegerField, ExpressionWrapper
import datetime

DELETE_STATE_CHOICES = (
    ('Y', 'deleted'),
    ('N', 'notDeleted'),
)


class ProductCode(Code):
    CONTENT_TYPE_CHOICES = (
        ('전란', '전란'),
        ('난백', '난백'),
        ('난황', '난황'),
        ('X', '없음'),
    )

    OEM_TYPE_CHOICES = (
        ('N', 'N'),
        ('Y', 'Y'),
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

    CALCULATE_TYPE_CHOICES = (
        ('order', '주문'),
        ('manual', '수기'),
    )

    type = models.CharField(
        max_length=10,
        choices=CONTENT_TYPE_CHOICES,
        default='',
    )
    amount_kg = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    price = models.IntegerField()
    store_type = models.CharField(
        max_length=10,
        choices=STORE_TYPE_CHOICES,
        default=''
    )
    vat = models.IntegerField(default=0)
    expiration = models.IntegerField(default=0)
    oem = models.CharField(
        max_length=10,
        choices=OEM_TYPE_CHOICES,
        default='N'
    )
    calculation = models.CharField(
        max_length=10,
        choices=CALCULATE_TYPE_CHOICES,
        default='order'
    )

    def __str__(self):
        return self.codeName + '(' + self.code + ')'


class ProductMaster(models.Model):
    ymd = models.CharField(max_length=8)
    total_loss_openEgg = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    total_loss_insert = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    total_loss_clean = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    total_loss_fill = models.DecimalField(decimal_places=2, max_digits=19, default=0)

    def __str__(self):
        return self.ymd + '_생산마스터'


class ProductEgg(models.Model):
    EGG_TYPE_CHOICES = (
        ('할란', '할란'),
        ('할란사용', '할란사용'),
        ('공정품투입', '공정품투입'),
        ('공정품발생', '공정품발생'),
        ('공정품폐기', '공정품폐기'),
        ('미출고품사용', '미출고품사용'),
        ('미출고품투입', '미출고품투입'),
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
        '01209': 'RAW Tank 등급란 난백',
        '01213': 'RAW Tank 동물복지 유정란 전란',
        '01214': 'Past Tank 동물복지 유정란 전란'
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
    rawTank_amount = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    pastTank_amount = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    loss_insert = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    loss_openEgg = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    memo = models.TextField(blank=True, null=True)
    delete_state = models.CharField(
        max_length=2,
        choices=DELETE_STATE_CHOICES,
        default='N',
    )

    def __str__(self):
        return self.type + '_' + self.codeName + '(' + self.ymd + ')'

    @staticmethod
    def makeVaildinfo(productEggInfo, memo):  # ('이름','실제값') -> ('이름','실제값','메모')
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
                productEgg.save()

    @staticmethod
    def getLossOpenEggPercent(masterInstance):
        total_rawTank_amount = 0
        eggs = ProductEgg.objects.filter(master_id=masterInstance).filter(type='할란').order_by('id')
        last_item = len(eggs) - 1

        if len(eggs) > 0:
            for egg in eggs: total_rawTank_amount += egg.rawTank_amount
            total_loss_openEgg_last = masterInstance.total_loss_openEgg
            total_loss_insert_last = masterInstance.total_loss_insert

            try:
                for egg in eggs[:last_item]:
                    percent = egg.rawTank_amount / total_rawTank_amount
                    egg.loss_openEgg = round(masterInstance.total_loss_openEgg * percent, 2)
                    egg.loss_insert = round(masterInstance.total_loss_insert * percent, 2)
                    egg.save()
                    total_loss_openEgg_last -= egg.loss_openEgg
                    total_loss_insert_last -= egg.loss_insert
            except ZeroDivisionError:
                pass

            lastEgg = eggs.last()
            lastEgg.loss_openEgg = total_loss_openEgg_last
            lastEgg.loss_insert = total_loss_insert_last
            lastEgg.save()

    @staticmethod
    def percentSummary(start_date, end_date):
        total_EggAmount = Egg.getAmount(start_date, end_date)  # 중량
        processProduct_amount = ProductEgg.objects.values('type').filter(ymd__gte=start_date).filter(ymd__lte=end_date) \
            .filter(type='할란').annotate(tankAmount=Sum('rawTank_amount') + Sum('pastTank_amount'))
        openEggUse_amount = ProductEgg.objects.values('type').filter(ymd__gte=start_date).filter(ymd__lte=end_date) \
            .filter(type='할란사용').annotate(tankAmount=Sum('rawTank_amount') + Sum('pastTank_amount'))
        product_amount = Product.objects.values('type').filter(ymd__gte=start_date).filter(ymd__lte=end_date) \
            .filter(type='제품생산').filter(purchaseYmd=None).annotate(tankAmount=Sum('amount'))
        processProductCreate_amount = ProductEgg.objects.values('type').filter(ymd__gte=start_date).filter(
            ymd__lte=end_date) \
            .filter(type='공정품발생').annotate(tankAmount=Sum('rawTank_amount') + Sum('pastTank_amount'))
        processProductInsert_amount = ProductEgg.objects.values('type').filter(ymd__gte=start_date).filter(
            ymd__lte=end_date) \
            .filter(type='공정품투입').annotate(tankAmount=Sum('rawTank_amount') + Sum('pastTank_amount'))
        recallProductInsert_amount = ProductEgg.objects.values('type').filter(ymd__gte=start_date).filter(
            ymd__lte=end_date) \
            .filter(type='미출고품투입').annotate(tankAmount=Sum('rawTank_amount') + Sum('pastTank_amount'))

        if not total_EggAmount: total_EggAmount = 0
        processProduct_amount = processProduct_amount[0]['tankAmount'] if processProduct_amount else 0
        openEggUse_amount = openEggUse_amount[0]['tankAmount'] if openEggUse_amount else 0
        product_amount = product_amount[0]['tankAmount'] if product_amount else 0
        processProductCreate_amount = processProductCreate_amount[0]['tankAmount'] if processProductCreate_amount else 0
        processProductInsert_amount = processProductInsert_amount[0]['tankAmount'] if processProductInsert_amount else 0
        recallProductInsert_amount = recallProductInsert_amount[0]['tankAmount'] if recallProductInsert_amount else 0

        loss_clean_amount = Product.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date) \
            .filter(purchaseYmd=None).aggregate(loss_clean=Sum('loss_clean'))
        loss_fill_amount = Product.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date) \
            .filter(purchaseYmd=None).aggregate(loss_fill=Sum('loss_fill'))
        loss_insert_amount = ProductEgg.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date) \
            .aggregate(loss_insert=Sum('loss_insert'))
        loss_openEgg_amount = ProductEgg.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date) \
            .aggregate(loss_openEgg=Sum('loss_openEgg'))

        loss_clean_amount = loss_clean_amount['loss_clean'] if loss_clean_amount['loss_clean'] else 0
        loss_fill_amount = loss_fill_amount['loss_fill'] if loss_fill_amount['loss_fill'] else 0
        loss_insert_amount = loss_insert_amount['loss_insert'] if loss_insert_amount['loss_insert'] else 0
        loss_openEgg_amount = loss_openEgg_amount['loss_openEgg'] if loss_openEgg_amount['loss_openEgg'] else 0

        openEggPercent = round((processProduct_amount / total_EggAmount * 100), 2) if total_EggAmount > 0 else 0
        productPercent = round(
            ((product_amount + processProduct_amount + openEggUse_amount + processProductInsert_amount +
              processProductCreate_amount + recallProductInsert_amount) / total_EggAmount * 100), 2) \
            if total_EggAmount > 0 else 0
        lossTotal = loss_clean_amount + loss_fill_amount + loss_insert_amount + loss_openEgg_amount
        insertLoss = round((loss_insert_amount / total_EggAmount * 100), 2) if total_EggAmount > 0 else 0
        openEggLoss = round((loss_openEgg_amount / processProduct_amount * 100), 2) if processProduct_amount > 0 else 0

        result = {'openEggPercent': openEggPercent,
                  'productPercent': productPercent,
                  'lossTotal': lossTotal,
                  'insertLoss': insertLoss,
                  'openEggLoss': openEggLoss}
        return result

    @staticmethod
    def productEggQuery(**kwargs):
        checkBoxFilter = kwargs.get('checkBoxFilter', None)[0]
        if checkBoxFilter:
            checkBoxFilter = checkBoxFilter.split(',')
            checkBoxFilter = [name for name in checkBoxFilter if name != '제품생산']

        search_value = kwargs.get('search[value]', None)[0]
        start_date = kwargs.get('start_date', None)[0]
        end_date = kwargs.get('end_date', None)[0]

        queryset = ProductEgg.objects.values(
            'id', list_master_id=F('master_id'), list_ymd=F('ymd'),
            list_type=F('type'), list_code=F('code'), list_codeName=F('codeName'),
            list_rawTank_amount=F('rawTank_amount'), list_pastTank_amount=F('pastTank_amount'),
            list_amount=Value(0, DecimalField()), list_amount_kg=Value(0, DecimalField()),
            list_count=Value(0, IntegerField()), list_loss_openEgg=F('loss_openEgg'),
            list_loss_insert=F('loss_insert'), list_loss_clean=Value(0, DecimalField()),
            list_loss_fill=Value(0, DecimalField()), list_memo=F('memo')
        ).filter(ymd__gte=start_date).filter(ymd__lte=end_date)

        total = queryset.count()

        if search_value:
            queryset = queryset.filter(Q(codeName__icontains=search_value) |
                                       Q(memo__icontains=search_value))

        if checkBoxFilter:
            queryset = queryset.filter(type__in=checkBoxFilter)

        count = queryset.count()
        return {
            'items': queryset,
            'count': count,
            'total': total
        }


class Product(Detail):
    PRODUCT_TYPE_CHOICES = (
        ('제품생산', '제품생산'),
        ('미출고품사용', '미출고품사용'),
    )
    type = models.CharField(
        max_length=30,
        choices=PRODUCT_TYPE_CHOICES,
        default='제품생산',
    )
    master_id = models.ForeignKey(ProductMaster,
                                  on_delete=models.CASCADE,
                                  related_name='master_id')
    loss_clean = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    loss_fill = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    productCode = models.ForeignKey(ProductCode, on_delete=models.CASCADE,
                                    blank=True, null=True, related_name='productInfo')
    '''OEM 상품에 한해서 있는 필드'''
    purchaseYmd = models.CharField(max_length=8, blank=True, null=True)
    purchaseLocation = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='purchase_locationCode',
                                         blank=True, null=True)
    purchaseLocationName = models.CharField(max_length=255, blank=True, null=True)
    purchaseSupplyPrice = models.IntegerField(blank=True, null=True)
    purchaseVat = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.codeName + '(' + self.ymd + ')'

    @staticmethod
    def getLossProductPercent(masterInstance):
        total_product_amount = 0
        products = Product.objects.filter(master_id=masterInstance).filter(purchaseYmd=None) \
            .filter(type='제품생산').order_by('id')
        last_item = len(products) - 1

        if len(products) > 0:
            for product in products:
                total_product_amount += product.amount
            total_loss_clean_last = masterInstance.total_loss_clean
            total_loss_fill_last = masterInstance.total_loss_fill

            try:
                for product in products[:last_item]:
                    percent = product.amount / total_product_amount
                    product.loss_clean = round(masterInstance.total_loss_clean * percent, 2)
                    product.loss_fill = round(masterInstance.total_loss_fill * percent, 2)
                    product.save()
                    total_loss_clean_last -= product.loss_clean
                    total_loss_fill_last -= product.loss_fill
            except ZeroDivisionError:
                pass

            lastProduct = products.last()
            lastProduct.loss_clean = total_loss_clean_last
            lastProduct.loss_fill = total_loss_fill_last
            lastProduct.save()

    @staticmethod
    def productQuery(**kwargs):
        search_value = kwargs.get('search[value]', None)[0]
        start_date = kwargs.get('start_date', None)[0]
        end_date = kwargs.get('end_date', None)[0]

        queryset = Product.objects.values(
            'id', list_master_id=F('master_id'), list_ymd=F('ymd'),
            list_type=F('type'), list_code=F('code'), list_codeName=F('codeName'),
            list_rawTank_amount=Value(0, DecimalField()), list_pastTank_amount=Value(0, DecimalField()),
            list_amount=F('amount'), list_amount_kg=F('amount_kg'),
            list_count=F('count'), list_loss_openEgg=Value(0, DecimalField()),
            list_loss_insert=Value(0, DecimalField()), list_loss_clean=F('loss_clean'),
            list_loss_fill=F('loss_fill'), list_memo=F('memo')
        ).filter(ymd__gte=start_date).filter(ymd__lte=end_date).filter(purchaseYmd=None)

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

    @staticmethod
    def productOEMQuery(**kwargs):
        ORDER_COLUMN_CHOICES = Choices(
            ('0', 'id'),
            ('1', 'purchaseYmd'),
            ('2', 'ymd'),
            ('3', 'locationCode_code'),
            ('4', 'purchaseLocationName'),
            ('5', 'code'),
            ('6', 'codeName'),
            ('7', 'count'),
            ('8', 'purchaseSupplyPrice'),
            ('9', 'purchaseVat'),
            ('10', 'totalPrice'),
            ('11', 'memo'),
        )
        draw = int(kwargs.get('draw', None)[0])
        start = int(kwargs.get('start', None)[0])
        length = int(kwargs.get('length', None)[0])
        search_value = kwargs.get('search[value]', None)[0]
        order_column = kwargs.get('order[0][column]', None)[0]
        order = kwargs.get('order[0][dir]', None)[0]
        order_column = ORDER_COLUMN_CHOICES[order_column]
        start_date = kwargs.get('start_date', None)[0]
        end_date = kwargs.get('end_date', None)[0]

        queryset = Product.objects.all().annotate(locationCode_code=F('purchaseLocation__code')) \
            .annotate(totalPrice=F('purchaseSupplyPrice') + F('purchaseVat')) \
            .filter(ymd__gte=start_date).filter(ymd__lte=end_date).exclude(purchaseYmd=None)

        total = queryset.count()

        if search_value:
            queryset = queryset.filter(Q(purchaseLocation__codeName__icontains=search_value) |
                                       Q(codeName__icontains=search_value) |
                                       Q(memo__icontains=search_value))

        if order == 'desc':
            order_column = '-' + order_column

        count = queryset.count()
        queryset = queryset.order_by(order_column)[start:start + length]
        return {
            'items': queryset,
            'count': count,
            'total': total,
            'draw': draw
        }


class ProductAdmin(models.Model):
    RELEASE_TYPE_CHOICES = (
        ('생성', '생성'),
        ('판매', '판매'),
        ('샘플', '샘플'),
        ('증정', '증정'),
        ('자손', '자손'),
        ('반품', '반품'),
        ('이동', '이동'),
        ('미출고품사용', '미출고품사용'),
        ('재고조정', '재고조정'),
    )
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=19, default=0)
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
                                               productYmd=F('product_id__ymd'),
                                               storedLocationCode=F('location__code'),
                                               amount_kg=F('product_id__amount_kg'),
                                               storedLocationCodeName=F('location__codeName')) \
            .annotate(totalCount=Sum('count')) \
            .annotate(totalAmount=Cast(Sum('amount'), DecimalField(max_digits=20, decimal_places=2))) \
            .filter(totalCount__gt=0)

        # django orm '-' -> desc
        if order == 'desc':
            order_column = '-' + order_column

        total = queryset.count()

        if search_value:
            queryset = queryset.filter(Q(productCodeName__icontains=search_value) |
                                       Q(productYmd__icontains=search_value) |
                                       Q(storedLocationCodeName__icontains=search_value))

        count = queryset.count()
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
                                               productYmd=F('product_id__ymd'),
                                               storedLocationCode=F('location__code'),
                                               amount_kg=F('product_id__amount_kg'),
                                               storedLocationCodeName=F('location__codeName')) \
            .annotate(totalCount=Sum('count')) \
            .annotate(totalAmount=Cast(Sum('amount'), DecimalField(max_digits=20, decimal_places=2))) \
            .filter(storedLocationCode=storedLocationCode) \
            .filter(productCode=productCode) \
            .filter(totalCount__gt=0) \
            .order_by('productYmd')
        return queryset


class ProductUnitPrice(TimeStampedModel):
    locationCode = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location')
    productCode = models.ForeignKey(ProductCode, on_delete=models.CASCADE, related_name='product')
    price = models.DecimalField(decimal_places=1, max_digits=19, default=0)
    specialPrice = models.DecimalField(decimal_places=1, max_digits=19, default=0)
    delete_state = models.CharField(
        max_length=2,
        choices=DELETE_STATE_CHOICES,
        default='N',
    )

    def __str__(self):
        return f"{self.locationCode.codeName}_ {self.productCode.codeName}_{self.price}"

    @staticmethod
    def productUnitPriceQuery(**kwargs):

        ORDER_COLUMN_CHOICES = Choices(
            ('0', 'id'),
            ('1', 'locationCode'),
            ('2', 'locationCodeName'),
            ('3', 'productCode'),
            ('4', 'productCodeName'),
            ('5', 'price'),
            ('6', 'specialPrice'),
        )
        draw = int(kwargs.get('draw', None)[0])
        start = int(kwargs.get('start', None)[0])
        length = int(kwargs.get('length', None)[0])
        search_value = kwargs.get('search[value]', None)[0]
        order_column = kwargs.get('order[0][column]', None)[0]
        order = kwargs.get('order[0][dir]', None)[0]
        order_column = ORDER_COLUMN_CHOICES[order_column]
        locationCode = kwargs.get('location', None)[0]
        productCode = kwargs.get('product', None)[0]

        queryset = ProductUnitPrice.objects.annotate(
            locationCodeName=F('locationCode__codeName'),
            productCodeName=F('productCode__codeName'))

        total = queryset.count()

        if locationCode:
            queryset = queryset.filter(locationCode=Location.objects.get(code=locationCode))

        if productCode:
            queryset = queryset.filter(productCode=ProductCode.objects.get(code=productCode))

        if search_value:
            queryset = queryset.filter(Q(locationCodeName__icontains=search_value) |
                                       Q(productCodeName__icontains=search_value))

        count = queryset.count()

        if order == 'desc':
            order_column = '-' + order_column

        queryset = queryset.order_by(order_column)[start:start + length]
        return {
            'items': queryset,
            'count': count,
            'total': total,
            'draw': draw
        }


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
    delete_state = models.CharField(
        max_length=2,
        choices=DELETE_STATE_CHOICES,
        default='N',
    )

    def __str__(self):
        return f"{self.setProductCode.codeName}_{self.saleLocation.codeName}_{self.productCode.codeName}"

    @staticmethod
    def setProductMatchQuery(**kwargs):

        ORDER_COLUMN_CHOICES = Choices(
            ('0', 'id'),
            ('1', 'saleLocation'),
            ('2', 'saleLocationCodeName'),
            ('3', 'setProductCode'),
            ('4', 'setProductCodeName'),
            ('5', 'productCode'),
            ('6', 'productCodeName'),
            ('7', 'price'),
            ('8', 'count'),
        )
        draw = int(kwargs.get('draw', None)[0])
        start = int(kwargs.get('start', None)[0])
        length = int(kwargs.get('length', None)[0])
        search_value = kwargs.get('search[value]', None)[0]
        order_column = kwargs.get('order[0][column]', None)[0]
        order = kwargs.get('order[0][dir]', None)[0]
        order_column = ORDER_COLUMN_CHOICES[order_column]
        saleLocation = kwargs.get('location', None)[0]
        setProductCode = kwargs.get('setProduct', None)[0]

        queryset = SetProductMatch.objects.filter(setProductCode__delete_state='N').annotate(
            saleLocationCodeName=F('saleLocation__codeName'),
            setProductCodeName=F('setProductCode__codeName'),
            productCodeName=F('productCode__codeName'))

        total = queryset.count()

        if saleLocation:
            queryset = queryset.filter(saleLocation=Location.objects.get(code=saleLocation))

        if setProductCode:
            queryset = queryset.filter(setProductCode=SetProductCode.objects.get(code=setProductCode))

        if search_value:
            queryset = queryset.filter(Q(productCodeName__icontains=search_value))

        count = queryset.count()

        if order == 'desc':
            order_column = '-' + order_column

        queryset = queryset.order_by(order_column)[start:start + length]
        return {
            'items': queryset,
            'count': count,
            'total': total,
            'draw': draw
        }


class ProductOrder(Detail):
    PRODUCT_TYPE_CHOICES = (
        ('전란', '전란'),
        ('난백난황', '난백난황'),
    )
    DISPLAY_CHOICES = (
        ('Y', '진행중'),
        ('N', '마감')
    )
    type = models.CharField(
        max_length=30,
        choices=PRODUCT_TYPE_CHOICES,
        default='전란',
    )
    productCode = models.ForeignKey(ProductCode, on_delete=models.CASCADE)
    display_state = models.CharField(
        max_length=10,
        choices=DISPLAY_CHOICES,
        default='Y',
    )

    def __str__(self):
        return self.codeName + '(' + self.ymd + ')'

    @staticmethod
    def productOrderListQuery(kwargs: QueryDict) -> dict:
        ORDER_COLUMN_CHOICES = Choices(
            ('0', 'id'),
            ('1', 'ymd'),
            ('2', 'type'),
            ('3', 'display_state'),
            ('4', 'code'),
            ('5', 'codeName'),
            ('6', 'count'),
            ('7', 'amount'),
            ('8', 'memo'),
        )

        draw = int(kwargs.get('draw', None))
        start = int(kwargs.get('start', None))
        length = int(kwargs.get('length', None))
        search_value = kwargs.get('search[value]', None)
        order_column = kwargs.get('order[0][column]', None)
        order_column = ORDER_COLUMN_CHOICES[order_column]
        order = kwargs.get('order[0][dir]', None)
        start_date = kwargs.get('start_date', None)
        end_date = kwargs.get('end_date', None)

        queryset = ProductOrder.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date)

        total = queryset.count()

        if order == 'desc':
            order_column = '-' + order_column

        if search_value:
            queryset = queryset.filter(Q(memo__icontains=search_value) |
                                       Q(codeName__icontains=search_value))

        count = queryset.count()

        if length != -1:
            queryset = queryset.order_by(order_column)[start:start + length]
        else:
            queryset = queryset.order_by(order_column)
        return {
            'items': queryset,
            'count': count,
            'total': total,
            'draw': draw
        }


class ProductOrderPacking(models.Model):
    productOrderCode = models.ForeignKey(ProductOrder, on_delete=models.CASCADE, related_name='detail')
    orderLocationCode = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    orderLocationCodeName = models.CharField(max_length=255, blank=True, null=True)
    boxCount = models.IntegerField()
    eaCount = models.IntegerField()

    def __str__(self):
        return f'{self.orderLocationCodeName} {self.boxCount} 상자 {self.eaCount} 개'