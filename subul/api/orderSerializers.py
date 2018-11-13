from rest_framework import serializers
from core.models import Location
from order.models import Order

class OrderSerializer(serializers.ModelSerializer):
    setProduct = serializers.SerializerMethodField()
    totalPrice = serializers.SerializerMethodField()
    orderLocationCode = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('id', 'code', 'codeName', 'ymd', 'price', 'count', 'amount', 'memo','orderLocationCode',
                  'orderLocationName', 'amount_kg', 'type', 'setProduct', 'totalPrice', 'delete_state')

    def get_setProduct(self, obj):
        if obj.setProduct:
            setProduct = obj.setProduct.codeName
        else:
            setProduct = ""
        return setProduct

    def get_totalPrice(self, obj):
        return obj.price * obj.count

    def get_orderLocationCode(self, obj):
        return obj.orderLocationCode.code


