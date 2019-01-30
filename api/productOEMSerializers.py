from rest_framework import serializers
from product.models import Product


class ProductOEMSerializer(serializers.ModelSerializer):
    locationCode_code = serializers.CharField(read_only=True)
    totalPrice = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
