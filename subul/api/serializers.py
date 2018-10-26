from rest_framework import serializers

from core.models import Location
from product.models import ProductMaster, Product, ProductEgg, ProductUnitPrice, SetProductMatch, SetProductCode, \
    ProductCode


class ProductSerializer(serializers.ModelSerializer):
    loss_insert = serializers.SerializerMethodField()
    loss_openEgg = serializers.SerializerMethodField()
    pastTank_amount = serializers.SerializerMethodField()
    rawTank_amount = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'master_id', 'ymd', 'code', 'codeName', 'amount', 'count', 'memo', 'loss_clean',
                  'loss_fill', 'delete_state',
                  'loss_insert', 'loss_openEgg', 'pastTank_amount', 'rawTank_amount', 'type')  # 가짜 데이터

    def get_loss_insert(self, obj):
        return None

    def get_loss_openEgg(self, obj):
        return None

    def get_pastTank_amount(self, obj):
        return None

    def get_rawTank_amount(self, obj):
        return None

    def get_type(self, obj):
        return '제품생산'


class ProductEggSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    loss_clean = serializers.SerializerMethodField()
    loss_fill = serializers.SerializerMethodField()

    class Meta:
        model = ProductEgg  # TODO tankName 필요!
        fields = ('id', 'master_id', 'ymd', 'type', 'code', 'codeName', 'rawTank_amount', 'pastTank_amount',
                  'loss_insert', 'loss_openEgg', 'memo', 'delete_state',
                  'code', 'codeName', 'amount', 'count', 'loss_clean', 'loss_fill')

    def get_amount(self, obj):
        return None

    def get_count(self, obj):
        return None

    def get_loss_clean(self, obj):
        return None

    def get_loss_fill(self, obj):
        return None


class ProductUnitPriceSerializer(serializers.ModelSerializer):
    codeName = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    amount_kg = serializers.SerializerMethodField()

    class Meta:
        model = ProductUnitPrice
        fields = ('id', 'price', 'code', 'codeName', 'amount_kg')

    def get_codeName(self, obj):
        return obj.productCode.codeName

    def get_code(self, obj):
        return obj.productCode.code

    def get_amount_kg(self, obj):
        return obj.productCode.amount_kg


class SetProductCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SetProductCode
        fields = ('code','codeName')


class ProductCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCode
        fields = ('code','codeName','amount_kg')


class SetProductMatchSerializer(serializers.ModelSerializer):
    code = serializers.SerializerMethodField()
    codeName = serializers.SerializerMethodField()
    amount_kg = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()

    class Meta:
        model = SetProductMatch
        fields = ('code', 'codeName', 'price', 'count', 'amount_kg', 'amount')

    def get_code(self, obj):
        return obj.productCode.code

    def get_codeName(self, obj):
        return obj.productCode.codeName

    def get_amount_kg(self, obj):
        return obj.productCode.amount_kg

    def get_amount(self, obj):
        return obj.productCode.amount_kg * obj.count



