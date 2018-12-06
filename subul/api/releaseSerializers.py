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
    contentType = serializers.CharField(read_only=True)
    kgPrice = serializers.FloatField(read_only=True)
    totalPrice = serializers.FloatField(read_only=True)
    supplyPrice = serializers.FloatField(read_only=True)
    eaPrice = serializers.IntegerField(read_only=True)
    releaseStoreLocationCodeName = serializers.CharField(read_only=True)
    orderMemo = serializers.CharField(read_only=True)
    locationType = serializers.SerializerMethodField(read_only=True)
    locationManagerName = serializers.CharField(read_only=True)
    releaseSetProduct = serializers.CharField(read_only=True)
    releaseSetProductCodeName = serializers.CharField(read_only=True)
    releaseLocationCode = serializers.SerializerMethodField()

    class Meta:
        model = Release
        fields = ('id', 'ymd', 'releaseLocationName', 'contentType', 'code', 'codeName', 'amount', 'count', 'amount_kg',
                  'kgPrice', 'price', 'totalPrice', 'supplyPrice', 'eaPrice', 'releaseVat', 'productYmd', 'type',
                  'releaseStoreLocationCodeName', 'orderMemo', 'locationType', 'locationManagerName',
                  'releaseSetProduct', 'releaseSetProductCodeName', 'specialTag', 'memo', 'releaseLocationCode',
                  'product_id')

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

    def get_releaseLocationCode(self, obj):
        return obj.releaseLocationCode.code
