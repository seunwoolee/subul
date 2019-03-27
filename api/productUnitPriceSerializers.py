from rest_framework import serializers
from product.models import ProductUnitPrice, SetProductMatch


class ProductUnitPriceListSerializer(serializers.ModelSerializer):
    locationCodeName = serializers.CharField(read_only=True)
    productCodeName = serializers.CharField(read_only=True)
    locationCode = serializers.SlugRelatedField(slug_field='code', read_only=True)
    productCode = serializers.SlugRelatedField(slug_field='code', read_only=True)

    class Meta:
        model = ProductUnitPrice
        fields = '__all__'


class SetProductMatchListSerializer(serializers.ModelSerializer):
    saleLocationCodeName = serializers.CharField(read_only=True)
    setProductCodeName = serializers.CharField(read_only=True)
    productCodeName = serializers.CharField(read_only=True)
    saleLocation = serializers.SlugRelatedField(slug_field='code', read_only=True)
    setProductCode = serializers.SlugRelatedField(slug_field='code', read_only=True)
    productCode = serializers.SlugRelatedField(slug_field='code', read_only=True)

    class Meta:
        model = SetProductMatch
        fields = '__all__'
