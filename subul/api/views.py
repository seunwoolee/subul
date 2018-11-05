from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins

from api.orderSerializers import OrderSerializer
from core.models import Location
from order.models import orderQuery, Order
from product.models import ProductMaster, Product, ProductEgg, productEggQuery, productQuery, ProductUnitPrice, \
    SetProductMatch, SetProductCode, ProductCode
from .serializers import ProductSerializer, ProductEggSerializer, ProductUnitPriceSerializer, SetProductCodeSerializer, \
    ProductCodeSerializer, SetProductMatchSerializer


# Create your views here.


class ProductsAPIView(APIView):

    def get(self, request, format=None):

        ORDER_COLUMN_CHOICES = {
            '0': 'id',
            '1': 'master_id',
            '2': 'type',
            '3': 'code',
            '4': 'codeName',
            '5': 'ymd',
            '6': 'amount',
            '7': 'count',
            '8': 'rawTank_amount',
            '9': 'pastTank_amount',
            '10': 'loss_insert',
            '11': 'loss_openEgg',
            '12': 'loss_clean',
            '13': 'loss_fill',
            '14': 'memo',
            '15': 'total_loss_insert'
        }
        order_column = request.query_params['order[0][column]']
        order_column = ORDER_COLUMN_CHOICES[order_column]
        start = int(request.query_params['start'])
        length = int(request.query_params['length'])
        draw = request.query_params['draw']

        order = request.query_params['order[0][dir]']

        product = productQuery(**request.query_params)
        productSerializer = ProductSerializer(product['items'], many=True)
        productEgg = productEggQuery(**request.query_params)
        productEggSerializer = ProductEggSerializer(productEgg['items'], many=True)
        mergedProductInfo = productEggSerializer.data + productSerializer.data

        if order == 'desc':
            mergedProductInfo = sorted(mergedProductInfo, key=lambda k: k[order_column] if k[order_column] != None
            else 0, reverse=True)  # ORDER BY
        else:
            mergedProductInfo = sorted(mergedProductInfo, key=lambda k: k[order_column] if k[order_column] != None
            else 0)  # ORDER BY

        result = dict()
        result['data'] = mergedProductInfo[start:start + length]  # 페이징
        result['draw'] = draw
        result['recordsTotal'] = product['total'] + productEgg['total']
        result['recordsFiltered'] = product['count'] + productEgg['count']
        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)


class OrdersAPIView(APIView):

    def get(self, request, format=None):
        try:
            orders = orderQuery(**request.query_params)
            orderSerializer = OrderSerializer(orders['items'], many=True)
            result = dict()
            result['data'] = orderSerializer.data
            result['draw'] = orders['draw']
            result['recordsTotal'] = orders['total']
            result['recordsFiltered'] = orders['count']
            print(result)
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)


class ProductUpdate(mixins.CreateModelMixin,
                    generics.UpdateAPIView):
    '''
    생산내역 조회에서 Update를 칠때 Patch
    '''

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        instance = Product.objects.get(pk=kwargs['pk'])
        self.partial_update(request, *args, **kwargs)
        Product.getLossProductPercent(instance.master_id)
        return Response(status=status.HTTP_200_OK)


class ProductCodes(APIView):
    '''
    You just need to provide the field which is to be modified.
    '''

    def get_object(self, code):
        try:
            return ProductCode.objects.get(code=code)
        except ProductCode.DoesNotExist:
            raise Http404

    def get(self, request, code, format=None):
        productCode = self.get_object(code)
        serializer = ProductCodeSerializer(productCode)
        return Response(serializer.data)


class ProductEggUpdate(mixins.CreateModelMixin,
                       generics.UpdateAPIView):
    '''
    생산내역 조회에서 Update를 칠때 Patch
    '''
    queryset = ProductEgg.objects.all()
    serializer_class = ProductEggSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        instance = ProductEgg.objects.get(pk=kwargs['pk'])
        self.partial_update(request, *args, **kwargs)
        ProductEgg.getLossOpenEggPercent(instance.master_id)
        return Response(status=status.HTTP_200_OK)


class OrderProductUnitPrice(APIView):
    """
    일반 상품일때 제품코드 , 코드명 , 가격, 키로수를 담고있음
    """

    def get_object(self, code):
        try:
            location = Location.objects.get(code=code)
            return ProductUnitPrice.objects.filter(locationCode=location)
            # return ProductUnitPrice.objects.all
        except ProductUnitPrice.DoesNotExist:
            raise Http404  # TODO 없으면 그냥 None

    def get(self, request, code, format=None):
        productUnitPrice = self.get_object(code)
        serializer = ProductUnitPriceSerializer(productUnitPrice, many=True)
        return Response(serializer.data)


class OrderSetProductCode(APIView):
    """
    패키지 상품일때 거래처 선택에 따라 제품명에 패키지 상품 추가(option)
    """

    def get_object(self, code):
        try:
            location = Location.objects.get(code=code)
            return SetProductCode.objects.filter(location=location).filter(delete_state='Y')
            # return ProductUnitPrice.objects.all
        except SetProductCode.DoesNotExist:
            raise Http404  # TODO 없으면 그냥 None

    def get(self, request, code, format=None):
        setProductCode = self.get_object(code)
        serializer = SetProductCodeSerializer(setProductCode, many=True)
        return Response(serializer.data)


class OrderSetProductMatch(APIView):
    """
    주문등록 - 패키지 상품일때 패키지상품 Match 값들을 가져와줌
    """

    def get_object(self, code):
        try:
            setProductCode = SetProductCode.objects.get(code=code)
            return SetProductMatch.objects.filter(setProductCode=setProductCode)
        except SetProductMatch.DoesNotExist:
            raise Http404

    def get(self, request, code, format=None):
        setProductMatch = self.get_object(code)
        serializer = SetProductMatchSerializer(setProductMatch, many=True)
        return Response(serializer.data)


class OrderUpdate(generics.UpdateAPIView):
    '''
    주문내역 조회에서 Update를 칠때 Patch
    '''

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
