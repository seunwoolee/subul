from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins

from api.orderSerializers import OrderSerializer
from api.releaseSerializers import ProductAdminSerializer, ReleaseSerializer
from core.models import Location
from eventlog.models import log
from order.models import Order
from product.models import ProductMaster, Product, ProductEgg, ProductUnitPrice, \
    SetProductMatch, SetProductCode, ProductCode, ProductAdmin
from release.models import Release
from .serializers import ProductSerializer, ProductEggSerializer, ProductUnitPriceSerializer, SetProductCodeSerializer, \
    ProductCodeSerializer, SetProductMatchSerializer, ProductMasterSerializer


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
            '14': 'memo'
        }
        order_column = request.query_params['order[0][column]']
        order_column = ORDER_COLUMN_CHOICES[order_column]
        start = int(request.query_params['start'])
        length = int(request.query_params['length'])
        draw = request.query_params['draw']
        order = request.query_params['order[0][dir]']
        checkBoxFilter = request.query_params['checkBoxFilter']
        mergedProductInfo = {}

        if checkBoxFilter == "제품생산":
            product = Product.productQuery(**request.query_params)
            productSerializer = ProductSerializer(product['items'], many=True)
            mergedProductInfo['total'] = product['total']
            mergedProductInfo['count'] = product['count']
            mergedProductInfo['data'] = productSerializer.data
        elif (checkBoxFilter and "제품생산" in checkBoxFilter) or not checkBoxFilter:
            productEgg = ProductEgg.productEggQuery(**request.query_params)
            productEggSerializer = ProductEggSerializer(productEgg['items'], many=True)
            product = Product.productQuery(**request.query_params)
            productSerializer = ProductSerializer(product['items'], many=True)
            mergedProductInfo['total'] = product['total'] + productEgg['total']
            mergedProductInfo['count'] = product['count'] + productEgg['count']
            mergedProductInfo['data'] = productEggSerializer.data + productSerializer.data
        else:  # 제품생산을 제외한 체크박스
            productEgg = ProductEgg.productEggQuery(**request.query_params)
            productEggSerializer = ProductEggSerializer(productEgg['items'], many=True)
            mergedProductInfo['total'] = productEgg['total']
            mergedProductInfo['count'] = productEgg['count']
            mergedProductInfo['data'] = productEggSerializer.data

        if order == 'desc':
            mergedProductInfo['data'] = sorted(mergedProductInfo['data'],
                                               key=lambda k: k[order_column] if k[order_column] != None
                                               else 0, reverse=True)
        else:
            mergedProductInfo['data'] = sorted(mergedProductInfo['data'],
                                               key=lambda k: k[order_column] if k[order_column] != None
                                               else 0)
        result = dict()
        result['data'] = mergedProductInfo['data'][start:start + length]  # 페이징
        result['draw'] = draw
        result['recordsTotal'] = mergedProductInfo['total']
        result['recordsFiltered'] = mergedProductInfo['count']
        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)


class OrdersAPIView(APIView):

    def get(self, request, format=None):
        try:
            orders = Order.orderQuery(**request.query_params)
            orderSerializer = OrderSerializer(orders['items'], many=True)
            result = dict()
            result['data'] = orderSerializer.data
            result['draw'] = orders['draw']
            result['recordsTotal'] = orders['total']
            result['recordsFiltered'] = orders['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)


class ProductUpdate(generics.RetrieveUpdateDestroyAPIView):
    '''
    생산내역 조회에서 Update를 칠때 Patch
    '''

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def patch(self, request, *args, **kwargs):
        instance = Product.objects.get(pk=kwargs['pk'])
        log(
            user=request.user,
            action="제품수정",
            obj=instance,
            extra={
                "name": instance.codeName,
                "amount": instance.amount,
                "count": instance.count
            }
        )
        self.partial_update(request, *args, **kwargs)
        Product.getLossProductPercent(instance.master_id)
        productAdmin = ProductAdmin.objects.filter(product_id=instance).filter(releaseType='생성').first()
        productAdmin.amount = request.data['amount']
        productAdmin.count = request.data['count']
        productAdmin.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = Product.objects.get(pk=kwargs['pk'])
        self.destroy(request, *args, **kwargs)
        Product.getLossProductPercent(instance.master_id)
        return Response(status=status.HTTP_200_OK)


class ProductMasterUpdate(mixins.CreateModelMixin,
                          generics.UpdateAPIView):
    '''
    생산등록에서 마스터 Update를 칠때 Patch
    '''

    queryset = ProductMaster.objects.all()
    serializer_class = ProductMasterSerializer
    lookup_field = 'ymd'

    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs, pk=None)
        instance = ProductMaster.objects.filter(ymd=kwargs['ymd']).first()
        Product.getLossProductPercent(instance)
        ProductEgg.getLossOpenEggPercent(instance)
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


class ProductEggUpdate(generics.RetrieveUpdateDestroyAPIView):
    '''
    생산내역 조회에서 Update, Delete를 칠때
    '''
    queryset = ProductEgg.objects.all()
    serializer_class = ProductEggSerializer

    def patch(self, request, *args, **kwargs):
        instance = ProductEgg.objects.get(pk=kwargs['pk'])
        self.partial_update(request, *args, **kwargs)
        ProductEgg.getLossOpenEggPercent(instance.master_id)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = ProductEgg.objects.get(pk=kwargs['pk'])
        self.destroy(request, *args, **kwargs)
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


class OrderUpdate(generics.RetrieveUpdateDestroyAPIView):
    """
    주문내역 조회에서 Update , Delete 할때 Delete 실행 시 주문에 물려있는 출고, 출고에 물려있는 재고(ProductAdmin) 삭제
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ReleaseUpdate(generics.RetrieveUpdateDestroyAPIView):
    """
    출고조회에서 Update , Delete 할때 Delete 실행 시 재고 TODO 정의필요
    """

    queryset = Release.objects.all()
    serializer_class = ReleaseSerializer


class ProductAdminsAPIView(APIView):

    def get(self, request, format=None):
        if self.checkOrderOrRelease(**request.query_params):
            try:
                productAdmins = ProductAdmin.productAdminQuery(**request.query_params)
                result = dict()
                result['data'] = productAdmins['items']
                print(result['data'])
                result['draw'] = productAdmins['draw']
                result['recordsTotal'] = productAdmins['total']
                result['recordsFiltered'] = productAdmins['count']
                return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
            except Exception as e:
                return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)
        else:
            storedLocationCode = request.query_params['storedLocation']
            productCode = request.query_params['code']
            productAdmins = ProductAdmin.productAdminOrderQuery(productCode, storedLocationCode)
            return Response(productAdmins, status=status.HTTP_200_OK, template_name=None, content_type=None)

    def checkOrderOrRelease(self, **kwargs):
        draw = kwargs.get('draw', None)
        if draw:
            return True
        else:
            return None


class ReleasesAPIView(APIView):

    def get(self, request, format=None):
        try:
            groupByFilter = request.query_params['groupByFilter']
            result = dict()
            if groupByFilter == 'stepOne':
                releases = Release.releaseQuery(**request.query_params)
                releaseSerializer = ReleaseSerializer(releases['items'], many=True)
                result['data'] = releaseSerializer.data
            else:
                releases = Release.releaseQuery(**request.query_params)
                result['data'] = releases['items']
            result['draw'] = releases['draw']
            result['recordsTotal'] = releases['total']
            result['recordsFiltered'] = releases['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)
