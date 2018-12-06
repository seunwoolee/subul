from rest_framework import serializers
from core.models import Location
from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    setProduct = serializers.SlugRelatedField(read_only=True, slug_field='codeName')
    setProductCode = serializers.CharField(read_only=True)
    totalPrice = serializers.IntegerField(read_only=True)
    orderLocationCode = serializers.SlugRelatedField(read_only=True, slug_field='code')
    release_id = serializers.SerializerMethodField(read_only=True)
    # 주문/출고실적 비교
    release_ymd = serializers.CharField(read_only=True)
    release_type = serializers.CharField(read_only=True)
    release_locationName = serializers.CharField(read_only=True)
    release_codeName = serializers.CharField(read_only=True)
    release_amount = serializers.CharField(read_only=True)
    release_count = serializers.CharField(read_only=True)
    release_price = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'code', 'codeName', 'ymd', 'price', 'count', 'amount', 'memo','orderLocationCode',
                  'orderLocationName', 'amount_kg', 'type', 'setProduct', 'totalPrice', 'delete_state',
                  'setProductCode', 'specialTag', 'release_id',
                  'release_ymd', 'release_type', 'release_locationName', 'release_codeName', 'release_amount',
                  'release_count', 'release_price')

    def get_release_id(self, obj):
        release_id = obj.release_id.id if obj.release_id else 0
        return release_id
