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


class ReleaseSerializer(serializers.ModelSerializer):
    contentType = serializers.CharField()
    kgPrice = serializers.FloatField()
    totalPrice = serializers.FloatField()
    supplyPrice = serializers.FloatField()
    eaPrice = serializers.IntegerField()
    releaseStoreLocationCodeName = serializers.CharField()
    orderMemo = serializers.CharField()
    locationType = serializers.SerializerMethodField()
    locationManagerName = serializers.CharField()
    releaseSetProduct = serializers.CharField()
    releaseSetProductCodeName = serializers.CharField()

    class Meta:
        model = Release
        fields = ('id', 'ymd', 'releaseLocationName', 'contentType', 'code', 'codeName', 'amount', 'count',
                  'kgPrice', 'totalPrice', 'supplyPrice', 'eaPrice', 'releaseVat', 'productYmd', 'type',
                  'releaseStoreLocationCodeName', 'orderMemo', 'locationType', 'locationManagerName',
                  'releaseSetProduct', 'releaseSetProductCodeName')

    def get_locationType(self, obj):
        CHARACTER_TYPE_CHOICES = {
            '01': 'B2B',
            '02': '급식',
            '03': '미군납',
            '04': '백화점',
            '05': '온라인',
            '06': '자사몰',
            '07': '직거래',
            '08': '특판',
            '09': '하이퍼',
            '99': '기타',
        }
        return CHARACTER_TYPE_CHOICES[obj.releaseLocationCode.location_character]
