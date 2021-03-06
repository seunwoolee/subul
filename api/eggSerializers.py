from rest_framework import serializers
from eggs.models import Egg, EggOrder


class EggSerializer(serializers.ModelSerializer):
    counts = serializers.IntegerField(read_only=True)
    in_price = serializers.IntegerField(read_only=True)
    out_price = serializers.IntegerField(read_only=True)
    pricePerEa = serializers.DecimalField(read_only=True, decimal_places=2, max_digits=19)
    in_locationCodes = serializers.CharField(read_only=True)
    locationCode = serializers.SlugRelatedField(
        slug_field='code',
        read_only=True
     )

    class Meta:
        model = Egg
        fields = '__all__'


class EggOrderSerializer(serializers.ModelSerializer):
    type = serializers.CharField(read_only=True)

    class Meta:
        model = EggOrder
        fields = '__all__'
