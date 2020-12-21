from django.contrib.auth.models import User
from django.db.models import F, Sum, Q, Max, IntegerField, Value, Count
from django.http import Http404, HttpResponse
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.forms.models import model_to_dict

from api.autoPackingSerializers import AutoPackingSerializer
from api.eggSerializers import EggSerializer, EggOrderSerializer
from api.locationSerializers import LocationSerializer
from api.orderSerializers import OrderSerializer, OrderDatatableSerializer
from api.packingSerializers import PackingSerializer
from api.productCodeSerializers import ProductCodeDatatableSerializer
from api.productOEMSerializers import ProductOEMSerializer
from api.productOrderSerializers import ProductOrderSerializer, ProductOrderPackingSerializer
from api.productUnitPriceSerializers import ProductUnitPriceListSerializer, SetProductMatchListSerializer
from api.releaseSerializers import ReleaseSerializer, CarDatatableSerializer, LocationDatatableSerializer
from core.models import Location
from eggs.models import Egg, EggOrder
from eventlog.models import LogginMixin
from order.models import Order
from packing.models import Packing, AutoPacking
from product.models import Product, ProductEgg, ProductUnitPrice, \
    SetProductMatch, SetProductCode, ProductCode, ProductAdmin, ProductOrder, ProductOrderPacking
from product.views import ProductOrderList
from release.models import Release, Car, OrderList
from release.services import CarServices
from .serializers import ProductSerializer, ProductEggSerializer, ProductUnitPriceSerializer, SetProductCodeSerializer, \
    ProductCodeSerializer, SetProductMatchSerializer


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

        if length > 0:
            mergedProductInfo['data'] = mergedProductInfo['data'].order_by(order_column)[start:start + length]
        else:
            mergedProductInfo['data'] = mergedProductInfo['data'].order_by(order_column)

        result = dict()
        result['data'] = mergedProductInfo['data']
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
        gubun_filter = request.query_params.get("gubunFilter", None)
        try:
            request.GET = request.GET.copy()
            request.GET['user_instance'] = request.user
            orders = Order.orderQuery(**request.GET)
            if gubun_filter == "stepTwo":
                result['data'] = orders['items']
            else:
                orderSerializer = OrderSerializer(orders['items'], many=True)
                result['data'] = orderSerializer.data
            result['draw'] = orders['draw']
            result['recordsTotal'] = orders['total']
            result['recordsFiltered'] = orders['count']

            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)


class OrderExAPIView(generics.ListAPIView):

    serializer_class = OrderDatatableSerializer

    def get_queryset(self):
        start_date = self.request.query_params["start_date"]
        end_date = self.request.query_params["end_date"]
        user: User = self.request.user
        orderLocationCode = Location.objects.filter(code=user.first_name).first()

        queryset = Order.objects.filter(Q(ymd__gte=start_date),
                                        Q(ymd__lte=end_date),
                                        Q(orderLocationCode=orderLocationCode))\
            .annotate(totalPrice=Sum(F('count') * F('price'), output_field=IntegerField())) \
            .annotate(setProductCode=F('setProduct__code'))

        return queryset


class ProductUpdate(LogginMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    생산내역 조회에서 Update
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def patch(self, request, *args, **kwargs):
        instance = Product.objects.get(pk=kwargs['pk'])
        self.log(
            user=request.user,
            action="제품수정",
            obj=instance,
            extra=model_to_dict(instance)
        )
        self.partial_update(request, *args, **kwargs)
        Product.getLossProductPercent(instance.master_id)
        productAdmin = ProductAdmin.objects.filter(product_id=instance).filter(releaseType='생성').first()
        productAdmin.amount = request.data['amount']
        productAdmin.count = request.data['count']
        productAdmin.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs) -> Response:
        instance: Product = Product.objects.get(pk=kwargs['pk'])
        self.log(
            user=request.user,
            action="제품삭제",
            obj=instance,
            extra=model_to_dict(instance)
        )
        if instance.type == "미출고품사용":
            origin_instance = Product.objects.filter(ymd=instance.ymd).filter(code=instance.code).filter(
                type="제품생산").first()
            ProductAdmin.objects.filter(product_id=origin_instance).filter(releaseType="미출고품사용").delete()
            self.destroy(request, *args, **kwargs)
        else:
            self.destroy(request, *args, **kwargs)
            Product.getLossProductPercent(instance.master_id)
        return Response(status=status.HTTP_200_OK)


class DeleteSelectedRows(LogginMixin, generics.DestroyAPIView):
    """
    생산내역조회 - 선택한 Rows 모두 삭제
    """

    def delete(self, request, *args, **kwargs):
        self.log(
            user=request.user,
            action="생산내역 일괄삭제",
            obj=ProductEgg.objects.first(),
        )
        product_data = request.data.getlist('product_data[]')
        productEgg_data = request.data.getlist('productEgg_data[]')

        Product.objects.filter(id__in=product_data).delete()
        ProductEgg.objects.filter(id__in=productEgg_data).delete()

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


class ProductCodeByPk(APIView):
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return ProductCode.objects.get(pk=pk)
        except ProductCode.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        productCode = self.get_object(pk)
        serializer = ProductCodeSerializer(productCode)
        return Response(serializer.data)


class ProductEggUpdate(LogginMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    생산내역 조회에서 Update, Delete
    """
    queryset = ProductEgg.objects.all()
    serializer_class = ProductEggSerializer

    def patch(self, request, *args, **kwargs):
        instance = ProductEgg.objects.get(pk=kwargs['pk'])
        self.log(
            user=request.user,
            action="액란수정",
            obj=instance,
            extra=model_to_dict(instance)
        )
        self.partial_update(request, *args, **kwargs)
        ProductEgg.getLossOpenEggPercent(instance.master_id)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = ProductEgg.objects.get(pk=kwargs['pk'])
        self.log(
            user=request.user,
            action="액란삭제",
            obj=instance,
            extra=model_to_dict(instance)
        )
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
        except ProductUnitPrice.DoesNotExist:
            raise Http404

    def get(self, request, code, format=None):
        if self.request.user.is_staff:
            return Response(status=404)

        productUnitPrice = self.get_object(code)
        serializer = ProductUnitPriceSerializer(productUnitPrice, many=True)
        return Response(serializer.data)


class OrderLocation(APIView):
    """
    주문등록 Delete 버튼 클릭 시 삭제된 location들 다시 append하기 위해
    장소명, 장소코드를 보내줌
    """

    def get(self, request, format=None):
        code = request.GET.get('code')
        if code:
            location = Location.objects.values('code', 'codeName').filter(type='05') \
                .filter(delete_state='N').exclude(code=code).order_by('code')
        else:
            location = Location.objects.values('code', 'codeName').filter(type='05') \
                .filter(delete_state='N').order_by('code')
        return Response(location)


class OrderSetProductCode(APIView):
    """
    패키지 상품일때 거래처 선택에 따라 제품명에 패키지 상품 추가(option)
    """

    def get_object(self, code):
        try:
            location = Location.objects.get(code=code)
            return SetProductCode.objects.filter(location=location).filter(delete_state='N')
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


class OrderUpdate(LogginMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    주문내역 조회에서 Update , Delete 할때 Delete 실행 시 주문에 물려있는 출고, 출고에 물려있는 재고(ProductAdmin) 삭제
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def patch(self, request, *args, **kwargs):
        instance = Order.objects.get(pk=kwargs['pk'])
        self.log(
            user=request.user,
            action="주문수정",
            obj=instance,
            extra=model_to_dict(instance)
        )
        self.partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = Order.objects.get(pk=kwargs['pk'])
        self.log(
            user=request.user,
            action="주문삭제",
            obj=instance,
            extra=model_to_dict(instance)
        )
        self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK)


class ReleaseUpdate(LogginMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    출고조회에서 Update , Delete
    """

    queryset = Release.objects.all()
    serializer_class = ReleaseSerializer

    def patch(self, request, *args, **kwargs):
        instance = Release.objects.get(pk=kwargs['pk'])
        self.log(
            user=request.user,
            action="출고수정",
            obj=instance,
            extra=model_to_dict(instance)
        )
        self.partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = Release.objects.get(pk=kwargs['pk'])
        self.log(
            user=request.user,
            action="출고삭제",
            obj=instance,
            extra=model_to_dict(instance)
        )
        self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK)


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

    def get(self, request):
        try:
            groupByFilter = request.query_params['groupByFilter']
            request.GET = request.GET.copy()
            request.GET['user_instance'] = request.user
            result = dict()
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


class EggsUpdate(LogginMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    원란조회에서 Update , Delete
    """

    queryset = Egg.objects.all()
    serializer_class = EggSerializer

    def patch(self, request, *args, **kwargs):
        instance = Egg.objects.get(pk=kwargs['pk'])
        egg = Egg.objects.filter(pk=kwargs['pk']).first()
        count = request.data.get('count', None)
        totalCount = Egg.objects.filter(in_locationCode=egg.in_locationCode).filter(code=egg.code).filter(
            in_ymd=egg.in_ymd).exclude(pk=kwargs['pk']).aggregate(Sum('count'))['count__sum'] or 0

        if int(totalCount) + int(count) >= 0:
            self.log(
                user=request.user,
                action="원란수정",
                obj=instance,
                extra=model_to_dict(instance)
            )
            self.partial_update(request, *args, **kwargs)
            return Response(status=status.HTTP_200_OK)
        else:
            self.log(
                user=request.user,
                action="원란수정실패",
                obj=instance,
                extra=model_to_dict(instance)
            )
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = Egg.objects.get(pk=kwargs['pk'])

        if instance.type == '입고':
            egg_releases = Egg.objects \
                .filter(Q(code=instance.code),
                        Q(in_ymd=instance.in_ymd),
                        ~Q(type='입고'),
                        Q(in_locationCode=instance.in_locationCode)) \
                .exclude(Q(id=instance.id))

            if egg_releases:
                ids = [str(egg_release.id) for egg_release in egg_releases]
                return HttpResponse(status=417, content=','.join(ids))

        self.log(
            user=request.user,
            action="원란삭제",
            obj=instance,
            extra=model_to_dict(instance)
        )
        self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK)


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


class PackingUpdate(LogginMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    원란조회에서 Update , Delete
    """

    queryset = Packing.objects.all()
    serializer_class = PackingSerializer

    def patch(self, request, *args, **kwargs):
        instance = Packing.objects.get(pk=kwargs['pk'])
        self.log(
            user=request.user,
            action="포장재수정",
            obj=instance,
            extra=model_to_dict(instance)
        )
        self.partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = Packing.objects.get(pk=kwargs['pk'])
        self.log(
            user=request.user,
            action="포장재삭제",
            obj=instance,
            extra=model_to_dict(instance)
        )
        self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK)


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
    OED 조회에서 Update , Delete
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
        if not specialPrice: specialPrice = 0
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
    """
    생산내역 조회에서 Update, Delete를 칠때
    """
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

    def post(self, request):
        location_instance = Location.objects.get(code=request.data['locationCode'])
        product_instance = ProductCode.objects.get(code=request.data['product'])
        setProduct_instance = SetProductCode.objects.get(code=request.data['setProductCode'])
        count = int(request.data['count'])
        price = request.data['price']
        SetProductMatch.objects.create(
            saleLocation=location_instance,
            productCode=product_instance,
            setProductCode=setProduct_instance,
            price=price,
            count=count
        )
        return Response(status=status.HTTP_201_CREATED, template_name=None, content_type=None)

        # if not SetProductMatch.objects.filter(saleLocation=location_instance) \
        #         .filter(productCode=product_instance).filter(setProductCode=setProduct_instance):
        #     SetProductMatch.objects.create(
        #         saleLocation=location_instance,
        #         productCode=product_instance,
        #         setProductCode=setProduct_instance,
        #         price=price,
        #         count=count
        #     )
        #     return Response(status=status.HTTP_201_CREATED, template_name=None, content_type=None)
        # else:
        #     return Response(status=status.HTTP_400_BAD_REQUEST, template_name=None, content_type=None)


class SetProductMatchsUpdate(generics.RetrieveUpdateDestroyAPIView):
    """
    생산내역 조회에서 Update, Delete를 칠때
    """
    queryset = SetProductMatch.objects.all()
    serializer_class = SetProductMatchListSerializer


class LocationsAPIView(APIView):

    def get(self, request):
        try:
            result = dict()
            location = Location.locationQuery(**request.query_params)
            locationSerializer = LocationSerializer(location['items'], many=True)
            result['data'] = locationSerializer.data
            result['draw'] = location['draw']
            result['recordsTotal'] = location['total']
            result['recordsFiltered'] = location['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)


class LocationUpdate(generics.RetrieveUpdateDestroyAPIView):
    """
    거래처 조회에서 Update
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class AutoPackingAPIView(APIView):

    def get(self, request):
        try:
            result = dict()
            autoPacking = AutoPacking.autoPackingQuery(**request.query_params)
            autoPackingSerializer = AutoPackingSerializer(autoPacking['items'], many=True)
            result['data'] = autoPackingSerializer.data
            result['draw'] = autoPacking['draw']
            result['recordsTotal'] = autoPacking['total']
            result['recordsFiltered'] = autoPacking['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)

    def post(self, request):
        serializer = AutoPackingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AutoPackingUpdate(generics.RetrieveUpdateDestroyAPIView):
    """
    포장재자동출고에서 Update, Delete를 칠때
    """
    queryset = AutoPacking.objects.all()
    serializer_class = AutoPackingSerializer


class EggOrderListAPIView(APIView):

    def get(self, request):
        try:
            result = dict()
            eggOrder = EggOrder.eggOrderListQuery(request.query_params)
            serializer = EggOrderSerializer(eggOrder['items'], many=True)
            result['data'] = serializer.data
            result['draw'] = eggOrder['draw']
            result['recordsTotal'] = eggOrder['total']
            result['recordsFiltered'] = eggOrder['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)


class EggOrderUpdate(generics.RetrieveUpdateDestroyAPIView):
    """
    원란지시조회에서 Update, Delete를 칠때
    """
    queryset = EggOrder.objects.all()
    serializer_class = EggOrderSerializer


class ProductOrderListAPIView(APIView):

    def get(self, request):
        try:
            result = dict()
            productOrder = ProductOrder.productOrderListQuery(request.query_params)
            serializer = ProductOrderSerializer(productOrder['items'], many=True)
            result['data'] = serializer.data
            result['draw'] = productOrder['draw']
            result['recordsTotal'] = productOrder['total']
            result['recordsFiltered'] = productOrder['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)
        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)

    def post(self, request):
        """
        생산지시서 popup 창에서 차주, 전주 재고 생성
        기존의 productOrder 에 재고가 있으면 412error 반환
        """
        origin_pk = request.data['pk']
        origin_instance: ProductOrder = ProductOrder.objects.get(pk=origin_pk)

        if request.data['type'] == '전주재고' and origin_instance.past_stock:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)

        if request.data['type'] == '차주재고' and origin_instance.future_stock:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)

        serializer = ProductOrderSerializer(data=request.data)
        if serializer.is_valid():
            instance: ProductOrder = serializer.save()

            if instance.type == '전주재고':
                origin_instance.past_stock = instance
            else:
                origin_instance.future_stock = instance

            origin_instance.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProductOrderUpdate(LogginMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    원란지시조회에서 Update, Delete를 칠때
    """
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer

    def delete(self, request, *args, **kwargs):
        instance = ProductOrder.objects.get(pk=kwargs['pk'])
        self.log(
            user=request.user,
            action="생산지시 삭제",
            obj=instance,
            extra=model_to_dict(instance)
        )

        if instance.type in ['전란', '난백난황']:
            if instance.future_stock:
                instance.future_stock.delete()

            if instance.past_stock:
                instance.past_stock.delete()

        self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK)


class ProductOrderPackingStockCreate(generics.ListCreateAPIView):
    queryset = ProductOrderPacking.objects.all()
    serializer_class = ProductOrderPackingSerializer

    def create(self, request, *args, **kwargs):
        if not request.data._mutable:
            request.data._mutable = True

        origin_productOrderPacking = ProductOrderPacking.objects.get(pk=request.data['origin_pk'])
        autoPacking = AutoPacking.objects.filter(Q(productCode=origin_productOrderPacking.productOrderCode.productCode),
                                                 Q(packingCode__type='외포장재')).first()

        if autoPacking:
            count = autoPacking.count
            mod, remainder = divmod(int(request.data['count']), count)
            request.data['boxCount'] = mod
            request.data['eaCount'] = remainder
            request.data['productOrderCode'] = origin_productOrderPacking.productOrderCode.id
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                instance: ProductOrderPacking = serializer.save()
                if request.data['stock_type'] == '전주재고':
                    origin_productOrderPacking.past_stock = instance
                else:
                    origin_productOrderPacking.future_stock = instance
                origin_productOrderPacking.save()
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            raise Http404


class ProductOrderReleaseStock(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        orderLocationCodeName = request.data.get('orderLocationCodeName', None)
        productOrder = ProductOrder.objects.get(pk=kwargs['pk'])
        mod_and_reminder: tuple = ProductOrderList.calculate_box_ea(productOrder)

        if productOrder.future.first():
            origin_productOrder = productOrder.future.first()
        else:
            origin_productOrder = productOrder.past.first()

        ProductOrderPacking.objects.create(
            type='일반',
            productOrderCode=origin_productOrder,
            boxCount=mod_and_reminder[0],
            eaCount=mod_and_reminder[1],
            orderLocationCodeName=orderLocationCodeName
        )
        return Response(status=status.HTTP_201_CREATED)


class ProductOrderPackingUpdate(LogginMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    생산지시서-팝업창에서 Update, Delete를 칠때
    """
    queryset = ProductOrderPacking.objects.all()
    serializer_class = ProductOrderPackingSerializer

    def delete(self, request, *args, **kwargs):
        instance = ProductOrderPacking.objects.get(pk=kwargs['pk'])
        self.log(
            user=request.user,
            action="생산지시 상세내용 삭제",
            obj=instance,
            extra=model_to_dict(instance)
        )

        self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        instance = ProductOrderPacking.objects.get(pk=kwargs['pk'])
        self.log(
            user=request.user,
            action="생산지시 상세내용 수정",
            obj=instance,
            extra=model_to_dict(instance)
        )

        self.partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK)


class ProductCodeDatatableList(generics.ListAPIView):
    """
    제품조회 DataTable List
    """
    queryset = ProductCode.objects.all()
    serializer_class = ProductCodeDatatableSerializer


class ProductCodeUpdate(generics.RetrieveUpdateAPIView):
    """
    제품조회 Update 칠때
    """
    queryset = ProductCode.objects.all()
    serializer_class = ProductCodeDatatableSerializer


class OrderPriceMatch(generics.ListAPIView):
    """
    주문조회 - 수정 - 특인 select Box 선택 시 정보 제공
    """

    serializer_class = ProductUnitPriceListSerializer

    def get_queryset(self):
        productCode = self.request.query_params['productCode']
        locationCode = self.request.query_params['locationCode']
        return ProductUnitPrice.objects.filter(Q(productCode__code=productCode), Q(locationCode__code=locationCode))


class CarDatatableList(generics.ListAPIView):
    """
    출고지시서 - 차량 DataTable List
    """
    queryset = Car.objects.all().annotate(pallet_count=Count(F('pallet')))
    serializer_class = CarDatatableSerializer


class CarCodeUpdate(LogginMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    출고지시서 - 차량 DataTable List
    """
    queryset = Car.objects.all()
    serializer_class = CarDatatableSerializer

    def delete(self, request, *args, **kwargs):
        instance = Car.objects.get(pk=kwargs['pk'])
        self.log(
            user=request.user,
            action="차량 삭제",
            obj=instance,
            extra=model_to_dict(instance)
        )

        self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        services = CarServices()
        pallet_count = int(request.data.get('pallet_count'))
        instance = Car.objects.get(pk=kwargs['pk'])
        self.log(
            user=request.user,
            action="차량 수정",
            obj=instance,
            extra=model_to_dict(instance)
        )
        self.partial_update(request, *args, **kwargs)

        if instance.pallet.count() != pallet_count:
            instance.pallet.all().delete()
            services.save_pallet(pallet_count, instance)

        return Response(status=status.HTTP_200_OK)


class LocationDatatableList(generics.ListAPIView):
    """
    출고지시서 - 차량 DataTable Click 시 해당일자에 주문이 1개 이상인 거래처 리스트 Display (DataTable)
    """
    serializer_class = LocationDatatableSerializer

    def get_queryset(self):
        ymd = self.request.query_params['ymd']
        return OrderList.objects.values(orderLocationCode=F('location'), orderLocationName=F('locationCodeName')) \
            .annotate(total_count=Count('id')).annotate(is_unloaded=Count('id', filter=Q(pallet__isnull=True))) \
            .filter(ymd=ymd).order_by('orderLocationName')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return Response(queryset.values('orderLocationCode', 'orderLocationName', 'total_count', 'is_unloaded'))


@api_view(['POST'])
def createAudit(request: Request):
    ymd: str = request.data.get('ymd')
    print(ymd)

