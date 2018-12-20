from django.db import models
from django.db.models import Q, F, ExpressionWrapper, FloatField, Sum, DecimalField
from django.db.models.functions import Cast
from model_utils import Choices
from core.models import Master, Detail, Location


class Release(Detail):
    RELEASE_TYPE_CHOICES = (
        ('판매', '판매'),
        ('샘플', '샘플'),
        ('증정', '증정'),
        ('자손', '자손'),
        ('반품', '반품'),
        ('이동', '이동'),
        ('미출고품', '미출고품'),
        ('재고조정', '재고조정'),
    )

    SPECIALTAG_TYPE_CHOICES = (
        ('', '일반'),
        ('특인가', '특인가'),
    )

    type = models.CharField(
        max_length=10,
        choices=RELEASE_TYPE_CHOICES,
        default='판매',
    )
    product_id = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='product', null=True,
                                   blank=True)
    productYmd = models.CharField(max_length=8)
    releaseLocationCode = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='release_locationCode')
    releaseLocationName = models.CharField(max_length=255)
    price = models.IntegerField()
    releaseOrder = models.ForeignKey('order.Order', on_delete=models.CASCADE, null=True, blank=True)
    releaseStoreLocation = models.ForeignKey(Location, on_delete=models.CASCADE,
                                             related_name='release_releaseStoreLocation')
    releaseSetProductCode = models.ForeignKey('product.SetProductCode', on_delete=models.CASCADE, null=True, blank=True)
    releaseVat = models.IntegerField()
    specialTag = models.CharField(
        max_length=10,
        choices=SPECIALTAG_TYPE_CHOICES,
        default='',
        blank=True
    )

    def __str__(self):
        return f"{self.codeName}_{self.type}_{self.releaseLocationName}"

    @staticmethod
    def releaseQuery(**kwargs):
        draw = int(kwargs.get('draw', None)[0])
        start = int(kwargs.get('start', None)[0])
        length = int(kwargs.get('length', None)[0])
        search_value = kwargs.get('search[value]', None)[0]
        start_date = kwargs.get('start_date', None)[0]
        end_date = kwargs.get('end_date', None)[0]
        order_column = kwargs.get('order[0][column]', None)[0]
        order = kwargs.get('order[0][dir]', None)[0]
        releaseTypeFilter = kwargs.get('releaseTypeFilter', None)[0]
        productTypeFilter = kwargs.get('productTypeFilter', None)[0]
        groupByFilter = kwargs.get('groupByFilter', None)[0]
        checkBoxFilter = kwargs.get('checkBoxFilter', None)[0]
        if checkBoxFilter: checkBoxFilter = checkBoxFilter.split(',')

        if groupByFilter == 'stepOne':
            RELEASE_COLUMN_CHOICES = Choices(
                ('0', 'id'),
                ('1', 'ymd'),
                ('2', 'releaseLocationName'),
                ('3', 'contentType'),
                ('4', 'specialTag'),
                ('5', 'code'),
                ('6', 'codeName'),
                ('7', 'amount'),
                ('8', 'count'),
                ('9', 'kgPrice'),
                ('10', 'totalPrice'),
                ('11', 'supplyPrice'),
                ('12', 'releaseVat'),
                ('13', 'eaPrice'),
                ('14', 'productYmd'),
                ('15', 'type'),
                ('16', 'releaseStoreLocationCodeName'),
                ('17', 'orderMemo'),
                ('18', 'memo'),
                ('19', 'locationType'),
                ('20', 'locationManagerName'),
                ('21', 'releaseSetProduct'),
                ('22', 'releaseSetProductCodeName'),
            )
            order_column = RELEASE_COLUMN_CHOICES[order_column]
            queryset = Release.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date).filter(delete_state='N') \
                .annotate(kgPrice=ExpressionWrapper(F('price') / F('amount'), output_field=FloatField())) \
                .annotate(contentType=F('product_id__productCode__type')) \
                .annotate(totalPrice=F('price')) \
                .annotate(supplyPrice=ExpressionWrapper(F('price') - F('releaseVat'), output_field=FloatField())) \
                .annotate(eaPrice=ExpressionWrapper(F('price') / F('count'), output_field=FloatField())) \
                .annotate(releaseStoreLocationCodeName=F('releaseStoreLocation__codeName')) \
                .annotate(orderMemo=F('releaseOrder__memo')) \
                .annotate(locationType=F('releaseLocationCode__location_character')) \
                .annotate(locationManagerName=F('releaseLocationCode__location_manager__first_name')) \
                .annotate(releaseSetProduct=F('releaseSetProductCode__code')) \
                .annotate(releaseSetProductCodeName=F('releaseSetProductCode__codeName'))
        elif groupByFilter == 'stepTwo':
            RELEASE_COLUMN_CHOICES = Choices(
                ('0', 'code'),
                ('1', 'specialTag'),
                ('2', 'codeName'),
                ('3', "type"),
                ('4', 'contentType'),
                ('5', 'amount'),
                ('6', 'count'),
                ('7', 'totalPrice'),
                ('8', 'kgPrice'),
                ('9', 'supplyPrice'),
                ('10', 'releaseVat'),
                ('11', "eaPrice"),
                ('12', "releaseStoreLocationCodeName")
            )
            order_column = RELEASE_COLUMN_CHOICES[order_column]
            queryset = Release.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date) \
                .filter(delete_state='N') \
                .values('code', 'codeName', 'type', 'specialTag') \
                .annotate(contentType=F('product_id__productCode__type')) \
                .annotate(amount=Sum('amount')) \
                .annotate(count=Sum('count')) \
                .annotate(totalPrice=Sum('price')) \
                .annotate(releaseVat=Sum('releaseVat')) \
                .annotate(kgPrice=Cast(F('totalPrice') / F('amount'), DecimalField(max_digits=20, decimal_places=2))) \
                .annotate(supplyPrice=ExpressionWrapper(F('totalPrice') - F('releaseVat'), output_field=FloatField())) \
                .annotate(eaPrice=ExpressionWrapper(F('totalPrice') / F('count'), output_field=FloatField())) \
                .annotate(releaseStoreLocationCodeName=F('releaseStoreLocation__codeName'))
        elif groupByFilter == 'stepThree':
            RELEASE_COLUMN_CHOICES = Choices(
                ('0', 'code'),
                ('1', 'specialTag'),
                ('2', 'codeName'),
                ('3', "type"),
                ('4', "releaseLocationName"),
                ('5', 'contentType'),
                ('6', 'amount'),
                ('7', 'count'),
                ('8', 'totalPrice'),
                ('9', 'kgPrice'),
                ('10', 'supplyPrice'),
                ('11', 'releaseVat'),
                ('12', "eaPrice"),
                ('13', "releaseStoreLocationCodeName")
            )
            order_column = RELEASE_COLUMN_CHOICES[order_column]
            queryset = Release.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date).filter(delete_state='N') \
                .values('code', 'codeName', 'type', 'specialTag') \
                .annotate(contentType=F('product_id__productCode__type')) \
                .annotate(releaseLocationName=F('releaseLocationName')) \
                .annotate(amount=Sum('amount')) \
                .annotate(count=Sum('count')) \
                .annotate(releaseVat=Sum('releaseVat')) \
                .annotate(totalPrice=Sum('price')) \
                .annotate(kgPrice=ExpressionWrapper(F('totalPrice') / F('amount'), output_field=FloatField())) \
                .annotate(supplyPrice=ExpressionWrapper(F('totalPrice') - F('releaseVat'), output_field=FloatField())) \
                .annotate(eaPrice=ExpressionWrapper(F('totalPrice') / F('count'), output_field=FloatField())) \
                .annotate(releaseStoreLocationCodeName=F('releaseStoreLocation__codeName'))
        elif groupByFilter == 'stepFour':
            RELEASE_COLUMN_CHOICES = Choices(
                ('0', 'releaseLocationName'),
                ('1', 'amount'),
                ('2', "count"),
                ('3', 'totalPrice'),
                ('4', 'supplyPrice'),
                ('5', 'releaseVat'),
            )
            order_column = RELEASE_COLUMN_CHOICES[order_column]
            queryset = Release.objects.filter(ymd__gte=start_date).filter(ymd__lte=end_date) \
                .filter(delete_state='N') \
                .values('releaseLocationName') \
                .annotate(amount=Sum('amount')) \
                .annotate(count=Sum('count')) \
                .annotate(totalPrice=Sum('price')) \
                .annotate(releaseVat=Sum('releaseVat')) \
                .annotate(supplyPrice=F('totalPrice') - F('releaseVat'))
        elif groupByFilter == 'stepFive':
            from django.apps import apps
            ProductAdmin = apps.get_model('product', 'ProductAdmin')
            RELEASE_COLUMN_CHOICES = Choices(
                ('0', 'id'),
                ('1', 'code'),
                ('2', "codeName"),
                ('3', 'ymd'),
                ('4', 'previousStock'),
                ('5', 'in'),
                ('6', 'sale'),
                ('7', 'sample'),
                ('8', 'broken'),
                ('9', 'notProduct'),
                ('10', 'recall'),
                ('11', 'currentStock'),
            )
            order_column = RELEASE_COLUMN_CHOICES[order_column]
            arr = []

            productAdmin = ProductAdmin.objects.values(  # 현재고
                productId=F('product_id__id'),
                productCode=F('product_id__code'),
                productCodeName=F('product_id__codeName'),
                oem=F('product_id__productCode__oem'),
                productYmd=F('ymd')).annotate(totalCount=Sum('count')).annotate(totalAmount=Sum('amount'))

            print(productAdmin)

            for product in productAdmin:
                result = {}
                countPerType = ProductAdmin.objects.values(productCode=F('product_id__code'),  # 타입별 출고 amount
                                                           productCodeName=F('product_id__codeName'),
                                                           productYmd=F('ymd'), type=F('releaseType')) \
                    .annotate(totalCount=Sum('count')) \
                    .annotate(totalAmount=Sum('amount')) \
                    .filter(product_id=product['productId']).filter(ymd__gte=start_date).filter(ymd__lte=end_date)
                CURRENT_STOCK = product['totalAmount'] if product['oem'] == 'N' else product["totalCount"]
                IN = 0
                SALE = 0
                SAMPLE = 0
                BROKEN = 0
                NOTPRODUCT = 0
                RECALL = 0

                for element in countPerType:
                    number = element["totalAmount"] if product['oem'] == 'N' else element["totalCount"]
                    if element['type'] == '생성':
                        IN += number
                    elif element['type'] == '판매':
                        SALE += number
                    elif element['type'] == '샘플' or element['type'] == '증정':
                        SAMPLE += number
                    elif element['type'] == '자손':
                        BROKEN += number
                    elif element['type'] == '미출고품':
                        NOTPRODUCT += number
                    elif element['type'] == '반품':
                        RECALL += number

                PREVIOUS_STOCK = '' if IN > 0 else CURRENT_STOCK - SALE - SAMPLE - BROKEN - NOTPRODUCT - RECALL # 기간
                # 내 생성이 된거면 전일재고는 당연히 없다
                if IN == 0: IN = ''
                if SALE == 0: SALE = ''
                if SAMPLE == 0: SAMPLE = ''
                if BROKEN == 0: BROKEN = ''
                if NOTPRODUCT == 0: NOTPRODUCT = ''
                if RECALL == 0: RECALL = ''
                if CURRENT_STOCK == 0: CURRENT_STOCK = ''
                result['id'] = product['productId']
                result['code'] = product['productCode']
                result['codeName'] = product['productCodeName']
                result['ymd'] = product['productYmd']
                result['previousStock'] = PREVIOUS_STOCK
                result['in'] = IN
                result['sale'] = SALE
                result['sample'] = SAMPLE
                result['broken'] = BROKEN
                result['notProduct'] = NOTPRODUCT
                result['recall'] = RECALL
                result['currentStock'] = CURRENT_STOCK
                # if not IN and not SALE and not SAMPLE and not BROKEN and not NOTPRODUCT and not RECALL and CURRENT_STOCK > 0:
                arr.append(result)
            return {
                'items': arr,
                'count': 10,
                'total': 10,
                'draw': draw
            }
        total = queryset.count()

        if releaseTypeFilter != '전체':
            queryset = queryset.filter(type=releaseTypeFilter)

        if productTypeFilter != '전체':
            queryset = queryset.filter(product_id__productCode__type=productTypeFilter)

        if checkBoxFilter:
            queryset = queryset.filter(releaseLocationCode__type__in=checkBoxFilter)

        if order == 'desc':
            order_column = '-' + order_column

        if search_value:
            queryset = queryset.filter(Q(code__icontains=search_value) |
                                       Q(codeName__icontains=search_value) |
                                       Q(memo__icontains=search_value))

        count = queryset.count()
        queryset = queryset.order_by(order_column)[start:start + length]
        return {
            'items': queryset,
            'count': count,
            'total': total,
            'draw': draw
        }
