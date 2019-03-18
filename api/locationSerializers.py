from rest_framework import serializers
from core.models import Location


class LocationSerializer(serializers.ModelSerializer):
    type_string = serializers.CharField(read_only=True)
    character_string = serializers.CharField(read_only=True)
    location_manager_string = serializers.CharField(read_only=True)

    class Meta:
        model = Location
        fields = ('id', 'code', 'codeName', 'type', 'location_address', 'location_phone', 'location_companyNumber',
                  'location_owner', 'location_shoppingmall', 'location_character', 'location_manager',
                  'type_string', 'character_string', 'location_manager_string')
