from rest_framework import serializers
from product.models import ProductOrder, ProductOrderPacking


class ProductOrderSerializer(serializers.ModelSerializer):
    real_count = serializers.IntegerField(read_only=True)
    real_amount = serializers.DecimalField(read_only=True, decimal_places=2, max_digits=19)

    class Meta:
        model = ProductOrder
        fields = '__all__'


class ProductOrderPackingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductOrderPacking
        fields = '__all__'
