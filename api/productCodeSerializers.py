from rest_framework import serializers
from product.models import ProductCode


class ProductCodeDatatableSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCode
        fields = ('id', 'code', 'codeName', 'type', 'amount_kg', 'calculation', 'expiration')
