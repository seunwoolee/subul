from rest_framework import serializers
from packing.models import AutoPacking


class AutoPackingSerializer(serializers.ModelSerializer):
    packingCodeName = serializers.CharField(read_only=True)
    productCodeName = serializers.CharField(read_only=True)

    class Meta:
        model = AutoPacking
        fields = '__all__'
