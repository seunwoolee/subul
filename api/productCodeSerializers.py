from rest_framework import serializers

from core.models import Audit
from product.models import ProductCode


class ProductCodeDatatableSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCode
        fields = ('id', 'code', 'codeName', 'type', 'amount_kg', 'calculation', 'expiration')


class AuditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Audit
        fields = '__all__'
