from rest_framework import serializers
from packing.models import Packing


class PackingSerializer(serializers.ModelSerializer):
    counts = serializers.IntegerField(read_only=True)
    locationCode_code = serializers.CharField(read_only=True)

    class Meta:
        model = Packing
        fields = '__all__'
