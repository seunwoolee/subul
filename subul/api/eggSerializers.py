from rest_framework import serializers
from eggs.models import Egg


class EggSerializer(serializers.ModelSerializer):
    in_locationCode = serializers.SerializerMethodField(read_only=True)
    locationCode = serializers.SerializerMethodField(read_only=True)
    in_price = serializers.SerializerMethodField(read_only=True)
    out_price = serializers.SerializerMethodField(read_only=True)
    pricePerEa = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Egg
        fields = ('id', 'type', 'code', 'codeName', 'count', 'in_ymd', 'in_locationCode', 'price',
                  'in_locationCodeName', 'locationCode', 'ymd', 'in_price', 'out_price', 'pricePerEa',
                  'locationCodeName', 'amount', 'memo')

    def get_in_locationCode(self, obj):
        in_locationCode = obj.in_locationCode.code if obj.in_locationCode else None
        return in_locationCode

    def get_locationCode(self, obj):
        locationCode = obj.locationCode.code if obj.locationCode else None
        return locationCode

    def get_in_price(self, obj):
        in_price = obj.price if obj.type == '입고' else None
        return in_price

    def get_out_price(self, obj):
        price = obj.price if obj.type != '입고' else None
        return price

    def get_pricePerEa(self, obj):
        price = round(obj.price / abs(obj.count)) if obj.price else None
        return price
