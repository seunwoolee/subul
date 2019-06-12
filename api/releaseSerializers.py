from rest_framework import serializers

from release.models import Release


class ReleaseSerializer(serializers.ModelSerializer):
    orderMemo = serializers.CharField(required=False)

    class Meta:
        model = Release
        fields = '__all__'

    def update(self, instance, validated_data):
        """
        출고조회 - 수정 시 ForeignKey Order의 메모 수정으로 overRide 실시(orderMemo)
        """
        instance.price = validated_data.get('price')
        instance.releaseVat = validated_data.get('releaseVat')
        instance.releaseOrder.memo = validated_data.get('orderMemo')
        instance.releaseOrder.save()
        instance.save()
        return instance


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
