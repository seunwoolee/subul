from rest_framework import serializers
from release.models import Release


class ReleaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Release
        fields = '__all__'


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
