from datetime import datetime
from rest_framework import serializers
from core.models import Location
from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    setProduct = serializers.SlugRelatedField(read_only=True, slug_field='codeName')
    setProductCode = serializers.CharField(read_only=True)
    totalPrice = serializers.IntegerField(read_only=True)
    orderLocationCode = serializers.SlugRelatedField(read_only=True, slug_field='code')
    release_id = serializers.SerializerMethodField(read_only=True)
    weekday = serializers.SerializerMethodField(read_only=True)
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
                  'setProductCode', 'specialTag', 'release_id', 'weekday',
                  'release_ymd', 'release_type', 'release_locationName', 'release_codeName', 'release_amount',
                  'release_count', 'release_price')

    def get_release_id(self, obj):
        release_id = obj.release_id.id if obj.release_id else 0
        return release_id

    def get_weekday(self, obj):
        WEEK_ARRAY = [
            '월',
            '화',
            '수',
            '목',
            '금',
            '토',
            '일'
        ]
        yyyy_mm_dd = '{}-{}-{}'.format(obj.ymd[0:4], obj.ymd[4:6], obj.ymd[6:8])
        weekday_index = datetime.strptime(yyyy_mm_dd, '%Y-%m-%d').weekday()
        return WEEK_ARRAY[weekday_index]