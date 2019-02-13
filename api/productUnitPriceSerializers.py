from rest_framework import serializers
from product.models import ProductUnitPrice


class ProductUnitPriceListSerializer(serializers.ModelSerializer):
    locationCodeName = serializers.CharField(read_only=True)
    productCodeName = serializers.CharField(read_only=True)
    locationCode = serializers.SlugRelatedField(
        slug_field='code',
        read_only=True
     )
    productCode = serializers.SlugRelatedField(
        slug_field='code',read_only=True
     )

    class Meta:
        model = ProductUnitPrice
        fields = '__all__'
