from rest_framework import serializers
from core.models import Location
from release.models import Release
from product.models import ProductAdmin, Product


class ProductAdminSerializer(serializers.Serializer):
    productId = serializers.IntegerField()
    productCode = serializers.CharField()
    productCodeName = serializers.CharField()
    productYmd = serializers.CharField()
    storedLocationCode = serializers.CharField()
    storedLocationCodeName = serializers.CharField()
    totalAmount = serializers.FloatField()
    totalCount = serializers.IntegerField()
    amount_kg = serializers.FloatField()
