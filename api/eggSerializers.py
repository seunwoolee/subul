from rest_framework import serializers
from eggs.models import Egg


class EggSerializer(serializers.ModelSerializer):
    counts = serializers.IntegerField(read_only=True)
    in_price = serializers.IntegerField(read_only=True)
    out_price = serializers.IntegerField(read_only=True)
    pricePerEa = serializers.DecimalField(read_only=True, decimal_places=2, max_digits=19)
    in_locationCodes = serializers.CharField(read_only=True)

    class Meta:
        model = Egg
        fields = '__all__'
