from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from product.models import ProductMaster, Product, ProductEgg, productEggQuery, productQuery
from .serializers import ProductSerializer, ProductEggSerializer


# Create your views here.


class ProductsAPIView(APIView):
    '''
    List Custom Product
    '''

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


class ProductUpdate(mixins.CreateModelMixin,
                    generics.UpdateAPIView):
    '''
    You just need to provide the field which is to be modified.
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


class ProductEggUpdate(mixins.CreateModelMixin,
                       generics.UpdateAPIView):
    '''
    You just need to provide the field which is to be modified.

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
