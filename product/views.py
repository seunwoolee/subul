from decimal import Decimal
from itertools import chain
from django.forms.models import model_to_dict
from django.db.models import Sum, F, Case, When, Value, CharField, Func, DecimalField, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from core.models import Location
from eggs.models import Egg
from eventlog.models import LogginMixin
from order.models import ABS, Order
from packing.forms import AutoPackingForm
from packing.models import AutoPacking, Packing, PackingCode
from product.codeForms import ProductUnitPricesForm, SetProductMatchForm, ProductCodeForm
from product.models import ProductEgg, Product, ProductCode, ProductAdmin, ProductMaster, ProductOrder, \
    ProductOrderPacking
from .forms import StepOneForm, StepTwoForm, StepThreeForm, StepFourForm, StepFourFormSet, MainForm, ProductOEMFormSet, \
    ProductOEMForm, ProductOrderForm, ProductOrderPackingForm, ProductOrderStockForm, ProductOrderPackingStockForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class ProductRegister(LogginMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'product.add_product'

    def post(self, request):
        global product, main
        form0 = MainForm(request.POST)
        form1 = StepOneForm(request.POST)
        form2 = StepTwoForm(request.POST)
        form3 = StepThreeForm(request.POST)
        formset = StepFourFormSet(request.POST)

        if form0.is_valid():
            main = form0.save()
            self.log(
                user=request.user,
                action="제품생산",
                obj=main,
                extra=model_to_dict(main)
            )

        if form1.is_valid():
            stepOneProductEgg = [[key, value] for key, value in form1.cleaned_data.items()]
            memo = [stepOneProductEgg[i][1] for i in range(2, len(stepOneProductEgg), 3)]  # 메모만 가져오기
            validStepOne = ProductEgg.makeVaildinfo(stepOneProductEgg, memo)
            ProductEgg.insertInfo(main, validStepOne)
            ProductEgg.getLossOpenEggPercent(main)

        if form2.is_valid():
            stepTwoProductEgg = [[key, value] for key, value in form2.cleaned_data.items()]
            memo = [stepTwoProductEgg[i][1] for i in range(1, len(stepTwoProductEgg), 2)]
            validStepTwo = ProductEgg.makeVaildinfo(stepTwoProductEgg, memo)
            ProductEgg.insertInfo(main, validStepTwo)

        if form3.is_valid():
            stepThreeProductEgg = [[key, value] for key, value in form3.cleaned_data.items()]
            memo = [stepThreeProductEgg[i][1] for i in range(1, len(stepThreeProductEgg), 2)]
            validStepThree = ProductEgg.makeVaildinfo(stepThreeProductEgg, memo)
            ProductEgg.insertInfo(main, validStepThree)

        if formset.is_valid():
            for form in formset:
                code = form.cleaned_data.get('product', None)
                amount = form.cleaned_data.get('amount', None)
                amount_kg = form.cleaned_data.get('amount_kg', None)
                count = form.cleaned_data.get('count', None)
                memo = form.cleaned_data.get('memo', None)
                KCFRESH_LOCATION_CODE: str = '00301'
                location = Location.objects.get(code=KCFRESH_LOCATION_CODE)  # kcfresh 본사

                if code and count > 0:
                    productCode = ProductCode.objects.get(code=code)
                    productExist = Product.objects.filter(code=code).filter(ymd=main.ymd).first()
                    if not productExist:
                        product = Product.objects.create(
                            master_id=main,
                            ymd=main.ymd,
                            code=code,
                            codeName=productCode.codeName,
                            productCode=productCode,
                            amount=amount,
                            amount_kg=amount_kg,
                            count=count,
                            memo=memo
                        )

                        productAdmin = ProductAdmin.objects.create(
                            product_id=product,
                            amount=amount,
                            count=count,
                            ymd=main.ymd,
                            location=location,
                        )
                        product.save()
                        productAdmin.save()
                    else:
                        productExist.amount += Decimal(amount)
                        productExist.count += count
                        productExistAdmin = ProductAdmin.objects.filter(releaseType='생성') \
                            .filter(product_id=productExist).first()
                        productExistAdmin.amount += Decimal(amount)
                        productExistAdmin.count += count
                        productExist.save()
                        productExistAdmin.save()

                    for packing in AutoPacking.objects.filter(productCode=productCode):
                        packing_product = productExist if productExist else product
                        packing_count = int(count) // int(packing.count)
                        Packing.objects.create(
                            ymd=main.ymd,
                            type='생산',
                            code=packing.packingCode.code,
                            codeName=packing.packingCode.codeName,
                            count=-packing_count,
                            packingCode=packing.packingCode,
                            productCode=packing_product,
                            autoRelease='자동출고',
                        )

            Product.getLossProductPercent(main)
        return redirect('productList')

    def get(self, request):
        tankValue = list(ProductEgg.objects.values('code', 'codeName') \
                         .filter(delete_state='N').annotate(rawSum=Sum('rawTank_amount')) \
                         .annotate(pastSum=Sum('pastTank_amount')).order_by('code'))
        for tank in tankValue:
            if "RAW" in tank["codeName"]:
                tank["amount"] = tank["rawSum"]
            elif "Past" in tank["codeName"]:
                tank["amount"] = tank["pastSum"]

        stepOneForm = StepOneForm(auto_id=False)
        stepTwoForm = StepTwoForm(auto_id=False)
        stepThreeForm = StepThreeForm(auto_id=False)
        stepFourForm = StepFourFormSet(request.GET or None)
        mainForm = MainForm(auto_id=False)
        return render(request, 'product/productRegister.html', {'stepOneForm': stepOneForm,
                                                                'stepTwoForm': stepTwoForm,
                                                                'stepThreeForm': stepThreeForm,
                                                                'stepFourForm': stepFourForm,
                                                                'mainForm': mainForm,
                                                                'tankValue': tankValue})


class ProductList(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'product.change_product'

    def get(self, request):
        return render(request, 'product/productList.html')


class ProductOrderList(View):

    def get(self, request):
        productOrderForm = ProductOrderForm()
        return render(request, 'product/productOrder.html', {'productOrderForm': productOrderForm})

    def post(self, request):
        self.start_date = request.POST.get('start_date', None)
        self.end_date = request.POST.get('end_date', None)
        self.content_type = request.POST.get('content_type', None)

        if self.content_type:  # 주문기반 자동 생성
            self.get_order()
            self.set_productOrder()
        else:
            form = ProductOrderForm(request.POST)
            if form.is_valid():
                productOrder = form.save(commit=False)
                origin_productOrder:ProductOrder = ProductOrder.objects.\
                    filter(Q(ymd=productOrder.ymd), Q(productCode=productOrder.productCode)).first()
                if not origin_productOrder:
                    productOrder.code = productOrder.productCode.code
                    productOrder.codeName = productOrder.productCode.codeName
                    productOrder.amount_kg = productOrder.productCode.amount_kg
                    productOrder.save()
                else:
                    origin_productOrder.count += productOrder.count
                    origin_productOrder.amount += productOrder.amount
                    origin_productOrder.save()
                    productOrder = origin_productOrder

                if form.cleaned_data['orderLocationCode']:
                    if origin_productOrder:
                        self.calculate_box_with_location(form.cleaned_data, origin_productOrder)
                    else:
                        self.calculate_box_with_location(form.cleaned_data, productOrder)
                else:
                    self.calculate_box_without_location(productOrder)

        return HttpResponse(status=200)

    def get_order(self):
        self.queryset = Order.objects.filter(ymd__gte=self.start_date).filter(ymd__lte=self.end_date) \
            .filter(productCode__calculation='자동').values('code', 'codeName', 'amount_kg') \
            .annotate(content_type=F('productCode__type')) \
            .annotate(calculation=F('productCode__calculation')) \
            .annotate(amount=Sum('amount')) \
            .annotate(count=Sum('count'))

        if self.content_type == '전란':
            self.queryset = self.queryset.filter(productCode__type=self.content_type)
        else:
            self.queryset = self.queryset.filter(Q(productCode__type='난황') | Q(productCode__type='난백'))

    def set_productOrder(self):
        for query in self.queryset:
            productCode = ProductCode.objects.get(code=query['code'])
            productOrder = ProductOrder.objects.create(
                ymd=self.start_date,
                code=query['code'],
                codeName=query['codeName'],
                amount=query['amount'],
                amount_kg=productCode.amount_kg,
                count=query['count'],
                productCode=productCode,
                type=self.content_type
            )

            if query['amount_kg'] < Decimal(5):
                self.calculate_box_without_location(productOrder)

            orders = Order.objects.values('code', 'codeName', 'orderLocationCode', 'productCode') \
                .filter(ymd__gte=self.start_date).filter(ymd__lte=self.end_date).filter(code=query['code']) \
                .filter(amount_kg__gte=Decimal(5)) \
                .annotate(amount=Sum('amount')).annotate(count=Sum('count'))

            for order in orders:
                self.calculate_box_with_location(order, productOrder)

    def calculate_box_with_location(self, form, productOrder):
        """
         5kg 이상일때만 거래처+상자+EA
        """
        # productCode = ProductCode.objects.get(code=order['code'])
        autoPacking = AutoPacking.objects.filter(productCode=form['productCode']).filter(packingCode__type='외포장재').first()
        orderLocationCode = Location.objects.get(id=form['orderLocationCode'])

        if autoPacking:
            count = autoPacking.count
            mod, remainder = divmod(form['count'], count)
            ProductOrderPacking.objects.create(
                productOrderCode=productOrder,
                orderLocationCode=orderLocationCode,
                orderLocationCodeName=orderLocationCode.codeName,
                boxCount=mod,
                eaCount=remainder,
            )
        # else: # 외포장재 없음
        #     count = 1
        #     mod, remainder = divmod(int(order['amount']), count)
        #     print(mod, remainder)

    def calculate_box_without_location(self, productOrder):
        """
         5kg 미만 제품 상자 +kg
        """
        productCode = ProductCode.objects.get(code=productOrder.code)
        autoPacking = AutoPacking.objects.filter(productCode=productCode).filter(packingCode__type='외포장재').first()

        if autoPacking:
            count = autoPacking.count
            mod, remainder = divmod(productOrder.count, count)
            ProductOrderPacking.objects.create(
                productOrderCode=productOrder,
                boxCount=mod,
                eaCount=remainder
            )


class ProductOrderPopup(LogginMixin, LoginRequiredMixin, View):
    def get(self, request, pk):
        productOrder = ProductOrder.objects.get(pk=pk)
        productOrderPackings = ProductOrderPacking.objects.filter(Q(productOrderCode=productOrder), Q(type='일반'))
        productOrderStockForm = ProductOrderStockForm()
        productOrderPackingStockForm = ProductOrderPackingStockForm()
        data = {'productOrder': productOrder,
                'productOrderStockForm': productOrderStockForm,
                'productOrderPackings': productOrderPackings,
                'productOrderPackingStockForm': productOrderPackingStockForm,
                'form': ProductOrderPackingForm}
        return render(request, 'product/popup_productOrder.html', data)


class ProductOrderFinish(LogginMixin, LoginRequiredMixin, View):
    def post(self, request):
        data = request.POST.dict()
        self.log(
            user=request.user,
            action="생산지시서 마감",
            obj=ProductOrder.objects.first(),
            extra=data
        )

        productOrders = ProductOrder.objects.filter(ymd__gte=data['start_date']).filter(ymd__lte=data['end_date'])
        for productOrder in productOrders:
            productOrder.display_state = 'N'
            productOrder.save()

        return HttpResponse(status=200)


class ProductRecall(LogginMixin, View):

    def post(self, request, pk):

        CODE_TYPE_CHOICES = {
            '01201': 'RAW Tank 전란',
            '01202': 'RAW Tank 난황',
            '01203': 'RAW Tank 난백',
        }

        ymd = request.POST['ymd']
        amount = Decimal(request.POST['amount'])
        count = int(request.POST['count'])
        memo = request.POST['memo']
        KCFRESH_LOCATION_CODE = '00301'
        location = Location.objects.get(code=KCFRESH_LOCATION_CODE)  # kcfresh 본사
        product = Product.objects.get(pk=pk)
        totalCount = ProductAdmin.objects.filter(product_id=product).values('product_id__code') \
            .annotate(totalCount=Sum(F('count')))

        self.log(
            user=request.user,
            action="미출고품발생",
            obj=product,
            extra=model_to_dict(product)
        )

        if count <= int(totalCount[0]['totalCount']):
            Product.objects.create(
                ymd=product.ymd,
                code=product.code,
                codeName=product.codeName,
                type="미출고품사용",
                amount=-amount,
                count=-count,
                amount_kg=product.amount_kg,
                master_id=product.master_id,
                memo=memo,
                productCode=product.productCode
            )
            ProductAdmin.objects.create(
                product_id=product,
                amount=-amount,
                count=-count,
                ymd=ymd,
                location=location,
                releaseType='미출고품사용'
            )
            if product.productCode.type == "전란":
                egg_code = '01201'
                egg_codeName = CODE_TYPE_CHOICES['01201']
            elif product.productCode.type == "난황":
                egg_code = '01202'
                egg_codeName = CODE_TYPE_CHOICES['01202']
            else:
                egg_code = '01203'
                egg_codeName = CODE_TYPE_CHOICES['01203']

            ProductEgg.objects.create(
                code=egg_code,
                codeName=egg_codeName,
                ymd=ymd,
                type='미출고품사용',
                rawTank_amount=amount,
                master_id=product.master_id,
            )

            ProductEgg.objects.create(
                code=egg_code,
                codeName=egg_codeName,
                ymd=ymd,
                type='미출고품투입',
                rawTank_amount=-amount,
                master_id=product.master_id,
            )
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=403)


class ProductReport(View):

    def get(self, request):
        SORT_ARRAY = ['미출고품사용',
                      '미출고품투입',
                      '이동',
                      '합계기타',
                      '원란',
                      '합계원란',
                      '할란',
                      '합계할란',
                      '할란사용',
                      '합계할란사용',
                      '공정품투입',
                      '합계공정품투입',
                      '공정품발생',
                      '합계공정품발생',
                      '공정품폐기',
                      '합계공정품폐기',
                      '제품생산',
                      '합계제품생산']
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        egg = Egg.objects.values('code', 'codeName').filter(ymd__gte=start_date).filter(ymd__lte=end_date) \
            .filter(type='생산') \
            .annotate(report_egg_amount=Case(When(amount=None, then=Value(0, DecimalField())), default=ABS('amount'),
                                             output_field=DecimalField())) \
            .annotate(report_egg_count=ABS('count')) \
            .annotate(report_sort_type=Value('원란', CharField())) \
            .annotate(report_rawTank_amount=Value(' ', CharField())) \
            .annotate(report_pastTank_amount=Value(' ', CharField())) \
            .annotate(report_product_amount=Value(' ', CharField())).order_by('codeName')

        total_amount = egg.aggregate(Sum('report_egg_amount'))['report_egg_amount__sum']
        total_count = egg.aggregate(Sum('report_egg_count'))['report_egg_count__sum']
        if not total_amount: total_amount = ' '
        if not total_count: total_count = ' '
        for i, _ in enumerate(egg):
            if egg[i]['report_egg_amount'] == 0:
                egg[i]['report_egg_amount'] = ' '

        total_egg = [dict(code=' ',
                          codeName='합계',
                          report_sort_type='합계원란',
                          report_egg_amount=total_amount,
                          report_egg_count=total_count,
                          report_rawTank_amount=' ',
                          report_pastTank_amount=' ',
                          report_product_amount=' ')]
        if total_egg[0]['report_egg_amount'] == ' ' and total_egg[0]['report_egg_count'] == ' ':
            total_egg[0]['code'] = 'pass'

        productEgg = ProductEgg.objects.values('code', 'codeName') \
            .filter(ymd__gte=start_date).filter(ymd__lte=end_date) \
            .annotate(report_egg_amount=Value(' ', CharField())) \
            .annotate(report_egg_count=Value(' ', CharField())) \
            .annotate(report_sort_type=F('type')) \
            .annotate(report_rawTank_amount=F('rawTank_amount')) \
            .annotate(report_pastTank_amount=F('pastTank_amount')) \
            .annotate(report_product_amount=Value(' ', CharField())).order_by('codeName')

        total_rawTank = productEgg.filter(report_sort_type='할란') \
            .aggregate(Sum('report_rawTank_amount'))['report_rawTank_amount__sum']
        total_pastTank = productEgg.filter(report_sort_type='할란') \
            .aggregate(Sum('report_pastTank_amount'))['report_pastTank_amount__sum']
        if not total_rawTank: total_rawTank = ' '
        if not total_pastTank: total_pastTank = ' '

        total_openEgg = [dict(code=' ',
                              codeName='합계',
                              report_sort_type='합계할란',
                              report_egg_amount=' ',
                              report_egg_count=' ',
                              report_rawTank_amount=total_rawTank,
                              report_pastTank_amount=total_pastTank,
                              report_product_amount=' ')]
        if total_openEgg[0]['report_rawTank_amount'] == ' ' and total_openEgg[0]['report_pastTank_amount'] == ' ':
            total_openEgg[0]['code'] = 'pass'

        total_rawTank = productEgg.filter(report_sort_type='할란사용') \
            .aggregate(Sum('report_rawTank_amount'))['report_rawTank_amount__sum']
        total_pastTank = productEgg.filter(report_sort_type='할란사용') \
            .aggregate(Sum('report_pastTank_amount'))['report_pastTank_amount__sum']
        if not total_rawTank: total_rawTank = ' '
        if not total_pastTank: total_pastTank = ' '

        total_openEggUse = [dict(code=' ',
                                 codeName='합계',
                                 report_sort_type='합계할란사용',
                                 report_egg_amount=' ',
                                 report_egg_count=' ',
                                 report_rawTank_amount=total_rawTank,
                                 report_pastTank_amount=total_pastTank,
                                 report_product_amount=' ')]
        if total_openEggUse[0]['report_rawTank_amount'] == ' ' and total_openEggUse[0]['report_pastTank_amount'] == ' ':
            total_openEggUse[0]['code'] = 'pass'

        total_rawTank = productEgg.filter(report_sort_type='공정품투입') \
            .aggregate(Sum('report_rawTank_amount'))['report_rawTank_amount__sum']
        total_pastTank = productEgg.filter(report_sort_type='공정품투입') \
            .aggregate(Sum('report_pastTank_amount'))['report_pastTank_amount__sum']
        if not total_rawTank: total_rawTank = ' '
        if not total_pastTank: total_pastTank = ' '

        total_insert = [dict(code=' ',
                             codeName='합계',
                             report_sort_type='합계공정품투입',
                             report_egg_amount=' ',
                             report_egg_count=' ',
                             report_rawTank_amount=total_rawTank,
                             report_pastTank_amount=total_pastTank,
                             report_product_amount=' ')]
        if total_insert[0]['report_rawTank_amount'] == ' ' and total_insert[0]['report_pastTank_amount'] == ' ':
            total_insert[0]['code'] = 'pass'

        total_rawTank = productEgg.filter(report_sort_type='공정품발생') \
            .aggregate(Sum('report_rawTank_amount'))['report_rawTank_amount__sum']
        total_pastTank = productEgg.filter(report_sort_type='공정품발생') \
            .aggregate(Sum('report_pastTank_amount'))['report_pastTank_amount__sum']
        if not total_rawTank: total_rawTank = ' '
        if not total_pastTank: total_pastTank = ' '

        total_create = [dict(code=' ',
                             codeName='합계',
                             report_sort_type='합계공정품발생',
                             report_egg_amount=' ',
                             report_egg_count=' ',
                             report_rawTank_amount=total_rawTank,
                             report_pastTank_amount=total_pastTank,
                             report_product_amount=' ')]
        if total_create[0]['report_rawTank_amount'] == ' ' and total_create[0]['report_pastTank_amount'] == ' ':
            total_create[0]['code'] = 'pass'

        total_rawTank = productEgg.filter(report_sort_type='공정품폐기') \
            .aggregate(Sum('report_rawTank_amount'))['report_rawTank_amount__sum']
        total_pastTank = productEgg.filter(report_sort_type='공정품폐기') \
            .aggregate(Sum('report_pastTank_amount'))['report_pastTank_amount__sum']
        if not total_rawTank: total_rawTank = ' '
        if not total_pastTank: total_pastTank = ' '

        total_remove = [dict(code=' ',
                             codeName='합계',
                             report_sort_type='합계공정품폐기',
                             report_egg_amount=' ',
                             report_egg_count=' ',
                             report_rawTank_amount=total_rawTank,
                             report_pastTank_amount=total_pastTank,
                             report_product_amount=' ')]
        if total_remove[0]['report_rawTank_amount'] == ' ' and total_remove[0]['report_pastTank_amount'] == ' ':
            total_remove[0]['code'] = 'pass'

        product = Product.objects.values('code', 'codeName').filter(ymd__gte=start_date).filter(ymd__lte=end_date) \
            .filter(purchaseYmd=None) \
            .annotate(report_egg_amount=Value(' ', CharField())) \
            .annotate(report_egg_count=Value(' ', CharField())) \
            .annotate(report_sort_type=F('type')) \
            .annotate(report_rawTank_amount=Value(' ', CharField())) \
            .annotate(report_pastTank_amount=Value(' ', CharField())) \
            .annotate(report_product_amount=F('amount')).order_by('codeName')

        total_amount = product.filter(report_sort_type='제품생산') \
            .aggregate(Sum('report_product_amount'))['report_product_amount__sum']
        if not total_amount: total_amount = ' '
        total_product = [dict(code=' ',
                              codeName='합계',
                              report_sort_type='합계제품생산',
                              report_egg_amount=' ',
                              report_egg_count=' ',
                              report_rawTank_amount=' ',
                              report_pastTank_amount=' ',
                              report_product_amount=total_amount)]
        if total_product[0]['report_product_amount'] == ' ':
            total_product[0]['code'] = 'pass'

        total_rawTank = productEgg.filter(report_sort_type__in=['미출고품사용', '미출고품투입']) \
            .aggregate(Sum('report_rawTank_amount'))['report_rawTank_amount__sum']
        total_amount = product.filter(report_sort_type='미출고품사용') \
            .aggregate(Sum('report_product_amount'))['report_product_amount__sum']

        if total_amount is None:
            total_amount = 0
        if total_rawTank is None:
            total_rawTank = 0
        total_other = [dict(code=' ',
                            codeName='합계',
                            report_sort_type='합계기타',
                            report_egg_amount=' ',
                            report_egg_count=' ',
                            report_rawTank_amount=total_rawTank,
                            report_pastTank_amount=' ',
                            report_product_amount=total_amount)]
        if total_other[0]['report_product_amount'] == 0 and total_other[0]['report_rawTank_amount'] == 0:
            total_other[0]['code'] = 'pass'
        result_list = sorted(
            chain(egg,
                  total_other,
                  total_egg,
                  productEgg,
                  total_openEgg,
                  total_openEggUse,
                  total_insert,
                  total_create,
                  total_remove,
                  product,
                  total_product),
            key=lambda x: SORT_ARRAY.index(x['report_sort_type']))
        percentSummary = ProductEgg.percentSummary(start_date, end_date)
        if len(result_list) > 37:
            first_loop_reuslt = result_list[:37]
            loop_reuslt = result_list[37:]
            return render(request, 'product/productReport.html',
                          {'first_loop_reuslt': first_loop_reuslt,
                           'loop_reuslt': loop_reuslt,
                           'percentSummary': percentSummary,
                           'start_date': start_date,
                           'end_date': end_date})
        else:
            return render(request, 'product/productReport.html', {'result_list': result_list,
                                                                  'percentSummary': percentSummary,
                                                                  'start_date': start_date,
                                                                  'end_date': end_date})


class ProductOEMReg(LoginRequiredMixin, View):

    def post(self, request):
        formset = ProductOEMFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                purchaseYmd = form.cleaned_data.get('purchaseYmd', None)
                ymd = form.cleaned_data.get('ymd', None)
                purchaseLocation = form.cleaned_data.get('location', None)
                purchaseSupplyPrice = form.cleaned_data.get('purchaseSupplyPrice', None)
                purchaseVat = form.cleaned_data.get('purchaseVat', None)
                code = form.cleaned_data.get('product', None)
                count = form.cleaned_data.get('count', None)
                memo = form.cleaned_data.get('memo', None)
                KCFRESH_LOCATION_CODE = '00301'
                location = Location.objects.get(code=KCFRESH_LOCATION_CODE)
                purchaseLocation = Location.objects.get(code=purchaseLocation)
                productCode = ProductCode.objects.get(code=code)
                main = ProductMaster.objects.filter(ymd='00000000').first()

                product = Product.objects.create(
                    master_id=main,
                    ymd=ymd,
                    code=code,
                    codeName=productCode.codeName,
                    productCode=productCode,
                    amount=count,
                    amount_kg=1,
                    count=count,
                    memo=memo,
                    purchaseYmd=purchaseYmd,
                    purchaseLocation=purchaseLocation,
                    purchaseLocationName=purchaseLocation.codeName,
                    purchaseSupplyPrice=purchaseSupplyPrice,
                    purchaseVat=purchaseVat
                )

                productAdmin = ProductAdmin.objects.create(
                    product_id=product,
                    amount=count,
                    count=count,
                    ymd=ymd,
                    location=location,
                )
                product.save()
                productAdmin.save()

        return redirect('productOEMList')

    def get(self, request):
        ProductOEMForm = ProductOEMFormSet(request.GET or None)
        return render(request, 'productOEM/productOEMReg.html', {'ProductOEMForm': ProductOEMForm})


class ProductOEMList(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'product.change_product'

    def get(self, request):
        productOEMForm = ProductOEMForm()
        return render(request, 'productOEM/productOEMList.html', {'productOEMForm': productOEMForm})


class ProductUnitPricesList(LoginRequiredMixin, View):

    def get(self, request):
        productUnitPricesForm = ProductUnitPricesForm()
        return render(request, 'code/productUnitPricesList.html', {'productUnitPricesForm': productUnitPricesForm})


class SetProductMatchList(LoginRequiredMixin, View):

    def get(self, request):
        productUnitPricesForm = SetProductMatchForm()
        return render(request, 'code/setProductMatchList.html', {'productUnitPricesForm': productUnitPricesForm})


class AutoPackingList(LoginRequiredMixin, View):

    def get(self, request):
        form = AutoPackingForm()
        return render(request, 'code/autoPackingList.html', {'form': form})


class ProductCodeList(LoginRequiredMixin, View):

    def get(self, request):
        form = ProductCodeForm()
        return render(request, 'code/productCodeList.html', {'form': form})
