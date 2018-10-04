from django.db import models
from core.models import Code, Detail, Location, Out , TimeStampedModel
from release.models import Release

class ProductMaster(models.Model):
    produce_id = models.IntegerField()
    ymd = models.CharField(max_length=8)
    total_loss_openEgg = models.IntegerField()
    total_loss_insert = models.IntegerField()
    total_loss_clean = models.IntegerField()
    total_loss_fill = models.IntegerField()
    total_openEgg = models.IntegerField()
    total_eggUse = models.IntegerField()
    total_storeInsert = models.IntegerField()
    total_produceStore = models.IntegerField()
    total_productAmount = models.IntegerField()
    total_productCount = models.IntegerField()


class ProductEgg(models.Model):
    EGG_TYPE_CHOICES= (
        ('할란', '할란'),
        ('할란사용', '할란사용'),
        ('공정품투입', '공정품투입'),
        ('공정품발생', '공정품발생'),
    )

    TANK_TYPE_CHOICES= (
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

    master_id = models.ForeignKey(ProductMaster,
                                  on_delete=models.CASCADE,
                                  related_name='temp')
    ymd = models.CharField(max_length=8)
    type = models.CharField(
        max_length=30,
        choices=EGG_TYPE_CHOICES,
        default='',
    )
    tank = models.CharField(
        max_length=10,
        choices=TANK_TYPE_CHOICES,
        default='01201'
    )
    rawTank_amount = models.IntegerField()
    pastTank_amount = models.IntegerField()
    loss_insert = models.FloatField()
    loss_openEgg = models.FloatField()
    memo = models.TextField()


class ProductCode(Code):
    CONTENT_TYPE_CHOICES= (
        ('전란', '전란'),
        ('난백', '난백'),
        ('난황', '난황'),
        ('', '없음'),
    )

    STORE_TYPE_CHOICES = (
        ('AP','AP'),
        ('BIB','BIB'),
        ('CT','CT'),
        ('PAC','PAC'),
        ('PKG','PKG'),
        ('TANK','TANK'),
        ('TON','TON'),
        ('TOTE','TOTE'),
        ('', '없음'),
    )

    type = models.CharField(
        max_length=10,
        choices=CONTENT_TYPE_CHOICES,
        default='',
    )

    amount_kg = models.IntegerField()
    price = models.IntegerField()
    store_type = models.CharField(
        max_length=10,
        choices=STORE_TYPE_CHOICES,
        default=''
    )
    vat = models.IntegerField(default=0)
    expiration = models.IntegerField(default=0)

    def __str__(self ):
        return self.code_name + ' ' + self.code


class Product(Detail): #TODO 주문 나갈때 Tag 붙이는 필드 필요
    master_id = models.ForeignKey(ProductMaster,
                                  on_delete=models.CASCADE,
                                  related_name='master_id')
    loss_clean = models.FloatField()
    loss_fill = models.FloatField()
    '''OEM 상품에 한해서 있는 필드'''
    purchaseYymd = models.CharField(max_length=8)
    purchaseLocation = models.ForeignKey(Location,on_delete=models.CASCADE,related_name='purchase_locationCode')
    purchaseLocationName = models.CharField(max_length=255)


class ProductAdmin(models.Model):
    RELEASE_TYPE_CHOICES = (
        ('판매','판매'),
        ('샘플','샘플'),
        ('증정','증정'),
        ('자손','자손'),
        ('이동','이동'),
    )
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    count = models.IntegerField()
    ymd = models.CharField(max_length=8)
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    releaseType = models.CharField(
        max_length=10,
        choices=RELEASE_TYPE_CHOICES,
        default='',
    )
    releaseSeq = models.ForeignKey(Release, on_delete=models.CASCADE)


class ProductUnitPrice(TimeStampedModel):
    locationCode = models.ForeignKey(Location, on_delete=models.CASCADE,related_name='location')
    productCode = models.ForeignKey(ProductCode, on_delete=models.CASCADE,related_name='product')
    price = models.IntegerField()


class SetProductMatch(TimeStampedModel):
    setProductCode = models.CharField(max_length=255)
    productCode = models.ForeignKey(ProductCode, on_delete=models.CASCADE)
    price = models.IntegerField()
    saleLocation = models.ForeignKey(Location, on_delete=models.CASCADE)


class SetProductCode(Code):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)