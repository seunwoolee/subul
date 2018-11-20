from rest_framework import serializers
from core.models import Location
from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    setProduct = serializers.SlugRelatedField(read_only=True, slug_field='codeName')
    setProductCode = serializers.CharField(read_only=True)
    totalPrice = serializers.IntegerField(read_only=True)
    orderLocationCode = serializers.SlugRelatedField(read_only=True, slug_field='code')

    class Meta:
        model = Order
        fields = ('id', 'code', 'codeName', 'ymd', 'price', 'count', 'amount', 'memo','orderLocationCode',
                  'orderLocationName', 'amount_kg', 'type', 'setProduct', 'totalPrice', 'delete_state',
                  'setProductCode', 'specialTag')

