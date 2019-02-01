from rest_framework import serializers

from core.models import Location
from product.models import ProductMaster, Product, ProductEgg, ProductUnitPrice, SetProductMatch, SetProductCode, \
    ProductCode


class ProductMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductMaster
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductEggSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductEgg
        fields = '__all__'


class ProductUnitPriceSerializer(serializers.ModelSerializer):
    codeName = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    amount_kg = serializers.SerializerMethodField()

    class Meta:
        model = ProductUnitPrice
        fields = ('id', 'price', 'code', 'codeName', 'amount_kg', 'specialPrice')

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
        fields = ('code', 'codeName', 'amount_kg')


class SetProductMatchSerializer(serializers.ModelSerializer):
    # orderLocationCode = serializers.SlugRelatedField(read_only=True, slug_field='code')
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



