from decimal import Decimal

from django.db.models import Sum
from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins

from api.eggSerializers import EggSerializer
from api.orderSerializers import OrderSerializer
from api.packingSerializers import PackingSerializer
from api.productOEMSerializers import ProductOEMSerializer
from api.productUnitPriceSerializers import ProductUnitPriceListSerializer, SetProductMatchListSerializer
from api.releaseSerializers import ProductAdminSerializer, ReleaseSerializer
from core.models import Location
from eggs.models import Egg
from eventlog.models import log
from order.models import Order
from packing.models import Packing
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
            '1': 'list_type',
            '2': 'list_code',
            '3': 'list_codeName',
            '4': 'list_ymd',
            '5': 'list_amount',
            '6': 'list_count',
            '7': 'list_rawTank_amount',
            '8': 'list_pastTank_amount',
            '9': 'list_loss_insert',
            '10': 'list_loss_openEgg',
            '11': 'list_loss_clean',
            '12': 'list_loss_fill',
            '13': 'list_memo'
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
            mergedProductInfo['total'] = product['total']
            mergedProductInfo['count'] = product['count']
            mergedProductInfo['data'] = product['items']
        elif (checkBoxFilter and "제품생산" in checkBoxFilter) or not checkBoxFilter:
            productEgg = ProductEgg.productEggQuery(**request.query_params)
            product = Product.productQuery(**request.query_params)
            mergedProductInfo['total'] = product['total'] + productEgg['total']
            mergedProductInfo['count'] = product['count'] + productEgg['count']
            mergedProductInfo['data'] = productEgg['items'].union(product['items'])
        else:  # 제품생산을 제외한 체크박스
            productEgg = ProductEgg.productEggQuery(**request.query_params)
            mergedProductInfo['total'] = productEgg['total']
            mergedProductInfo['count'] = productEgg['count']
            mergedProductInfo['data'] = productEgg['items']

        if order == 'desc':
            order_column = '-' + order_column

        mergedProductInfo['data'] = mergedProductInfo['data'].order_by(order_column)
        result = dict()
        result['data'] = mergedProductInfo['data'][start:start + length]
        result['draw'] = draw
        result['recordsTotal'] = mergedProductInfo['total']
        result['recordsFiltered'] = mergedProductInfo['count']
        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)


class ProductSummaryAPIView(APIView):

    def get(self, request, format=None):
        start_date = request.query_params["start_date"]
        end_date = request.query_params["end_date"]
        result = ProductEgg.percentSummary(start_date, end_date)
        return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)


class OrdersAPIView(APIView):

    def get(self, request, format=None):
        result = dict()
        try:
            if request.query_params.get("gubunFilter", None) != "stepThree":
                request.GET = request.GET.copy()
                request.GET['user_instance'] = request.user
                orders = Order.orderQuery(**request.GET)
                orderSerializer = OrderSerializer(orders['items'], many=True)
                result['data'] = orderSerializer.data
                result['draw'] = orders['draw']
                result['recordsTotal'] = orders['total']
                result['recordsFiltered'] = orders['count']
            else:
                result = Order.orderStepThreeQuery(**request.query_params)
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
        if instance.type == "미출고품사용":
            origin_instance = Product.objects.filter(ymd=instance.ymd).filter(code=instance.code).filter(
                type="제품생산").first()
            ProductAdmin.objects.filter(product_id=origin_instance).filter(releaseType="미출고품사용").delete()
            self.destroy(request, *args, **kwargs)
        else:
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
            raise Http404

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
            return SetProductCode.objects.filter(location=location).filter(delete_state='N')
            # return ProductUnitPrice.objects.all
        except SetProductCode.DoesNotExist:
            raise Http404

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
    출고조회에서 Update , Delete 할때 Delete 실행 시 재고
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
            request.GET = request.GET.copy()
            request.GET['user_instance'] = request.user
            result = dict()
            if groupByFilter == 'stepOne':
                releases = Release.releaseQuery(**request.GET)
                releaseSerializer = ReleaseSerializer(releases['items'], many=True)
                result['data'] = releaseSerializer.data
            else:
                releases = Release.releaseQuery(**request.GET)
                result['data'] = releases['items']
            result['draw'] = releases['draw']
            result['recordsTotal'] = releases['total']
            result['recordsFiltered'] = releases['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)


class EggsAPIView(APIView):

    def get(self, request, format=None):
        try:
            Eggs = Egg.eggQuery(**request.query_params)
            result = dict()
            result['data'] = Eggs['items']
            result['draw'] = Eggs['draw']
            result['recordsTotal'] = Eggs['total']
            result['recordsFiltered'] = Eggs['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)


class EggsListAPIView(APIView):

    def get(self, request, format=None):
        try:
            result = dict()
            Eggs = Egg.eggListQuery(**request.query_params)
            eggSerializer = EggSerializer(Eggs['items'], many=True)
            result['data'] = eggSerializer.data
            result['draw'] = Eggs['draw']
            result['recordsTotal'] = Eggs['total']
            result['recordsFiltered'] = Eggs['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)


class EggsReportAPIView(APIView):

    def get(self, request, format=None):
        try:
            result = dict()
            Eggs = Egg.eggReportQuery(**request.query_params)
            result['data'] = Eggs['items']
            result['draw'] = Eggs['draw']
            result['recordsTotal'] = Eggs['total']
            result['recordsFiltered'] = Eggs['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)


class EggsUpdate(generics.RetrieveUpdateDestroyAPIView):
    """
    원란조회에서 Update , Delete
    """

    queryset = Egg.objects.all()
    serializer_class = EggSerializer


class PackingListAPIView(APIView):

    def get(self, request):
        try:
            result = dict()
            Packings = Packing.packingListQuery(**request.query_params)
            packingSerializer = PackingSerializer(Packings['items'], many=True)
            result['data'] = packingSerializer.data
            result['draw'] = Packings['draw']
            result['recordsTotal'] = Packings['total']
            result['recordsFiltered'] = Packings['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)


class PackingUpdate(generics.RetrieveUpdateDestroyAPIView):
    """
    원란조회에서 Update , Delete
    """

    queryset = Packing.objects.all()
    serializer_class = PackingSerializer


class PackingAPIView(APIView):

    def get(self, request, format=None):
        try:
            Packings = Packing.packingQuery(**request.query_params)
            result = dict()
            result['data'] = Packings['items']
            result['draw'] = Packings['draw']
            result['recordsTotal'] = Packings['total']
            result['recordsFiltered'] = Packings['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)


class PackingReportAPIView(APIView):

    def get(self, request, format=None):
        try:
            result = dict()
            Packings = Packing.packingReportQuery(**request.query_params)
            result['data'] = Packings['items']
            result['draw'] = Packings['draw']
            result['recordsTotal'] = Packings['total']
            result['recordsFiltered'] = Packings['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)


class ProductOEMsAPIView(APIView):

    def get(self, request):
        try:
            result = dict()
            productOEM = Product.productOEMQuery(**request.query_params)
            productOEMSerializer = ProductOEMSerializer(productOEM['items'], many=True)
            result['data'] = productOEMSerializer.data
            result['draw'] = productOEM['draw']
            result['recordsTotal'] = productOEM['total']
            result['recordsFiltered'] = productOEM['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)


class ProductOEMUpdate(generics.RetrieveUpdateDestroyAPIView):
    """
    OEM조회에서 Update , Delete
    """

    queryset = Product.objects.all().exclude(purchaseYmd=None)
    serializer_class = ProductOEMSerializer


class ProductUnitPricesAPIView(APIView):

    def get(self, request):
        try:
            result = dict()
            productUnitPrice = ProductUnitPrice.productUnitPriceQuery(**request.query_params)
            productUnitPriceSerializer = ProductUnitPriceListSerializer(productUnitPrice['items'], many=True)
            result['data'] = productUnitPriceSerializer.data
            result['draw'] = productUnitPrice['draw']
            result['recordsTotal'] = productUnitPrice['total']
            result['recordsFiltered'] = productUnitPrice['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)

    def post(self, request):
        location_instance = Location.objects.get(code=request.data['locationCode'])
        product_instance = ProductCode.objects.get(code=request.data['productCode'])
        specialPrice = request.data['specialPrice']
        if not specialPrice: specialPrice=0
        if not ProductUnitPrice.objects.filter(locationCode=location_instance).filter(productCode=product_instance):
            ProductUnitPrice.objects.create(
                locationCode=location_instance,
                productCode=product_instance,
                price=request.data['price'],
                specialPrice=specialPrice
            )
            return Response(status=status.HTTP_201_CREATED, template_name=None, content_type=None)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, template_name=None, content_type=None)


class ProductUnitPricesUpdate(generics.RetrieveUpdateDestroyAPIView):
    '''
    생산내역 조회에서 Update, Delete를 칠때
    '''
    queryset = ProductUnitPrice.objects.all()
    serializer_class = ProductUnitPriceSerializer


class SetProductMatchsAPIView(APIView):

    def get(self, request):
        try:
            result = dict()
            setProductMatch = SetProductMatch.setProductMatchQuery(**request.query_params)
            setProductMatchListSerializer = SetProductMatchListSerializer(setProductMatch['items'], many=True)
            result['data'] = setProductMatchListSerializer.data
            result['draw'] = setProductMatch['draw']
            result['recordsTotal'] = setProductMatch['total']
            result['recordsFiltered'] = setProductMatch['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)

    # def post(self, request):
    #     location_instance = Location.objects.get(code=request.data['locationCode'])
    #     product_instance = ProductCode.objects.get(code=request.data['productCode'])
    #     specialPrice = request.data['specialPrice']
    #     if not specialPrice: specialPrice=0
    #     if not ProductUnitPrice.objects.filter(locationCode=location_instance).filter(productCode=product_instance):
    #         ProductUnitPrice.objects.create(
    #             locationCode=location_instance,
    #             productCode=product_instance,
    #             price=request.data['price'],
    #             specialPrice=specialPrice
    #         )
    #         return Response(status=status.HTTP_201_CREATED, template_name=None, content_type=None)
    #     else:
    #         return Response(status=status.HTTP_400_BAD_REQUEST, template_name=None, content_type=None)


class SetProductMatchsUpdate(generics.RetrieveUpdateDestroyAPIView):
    '''
    생산내역 조회에서 Update, Delete를 칠때
    '''
    queryset = SetProductMatch.objects.all()
    serializer_class = SetProductMatchListSerializer

