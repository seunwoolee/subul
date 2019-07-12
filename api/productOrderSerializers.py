from rest_framework import serializers
from product.models import ProductOrder, ProductOrderPacking


class ProductOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductOrder
        fields = '__all__'


class ProductOrderPackingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductOrderPacking
        fields = '__all__'
