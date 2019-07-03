from rest_framework import serializers
from product.models import ProductOrder


class ProductOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductOrder
        fields = '__all__'
