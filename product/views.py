from decimal import Decimal
from itertools import chain
from django.db.models import Sum, F, Case, When, Value, CharField, Func
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from core.models import Location
from eggs.models import Egg
from eventlog.models import log
from product.models import ProductEgg, Product, ProductCode, ProductAdmin, ProductMaster
from .forms import StepOneForm, StepTwoForm, StepThreeForm, StepFourForm, StepFourFormSet, MainForm, ProductOEMFormSet, \
    ProductOEMForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class ABS(Func):
    function = 'ABS'


class ProductRegister(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'product.add_product'

    def post(self, request):
        form0 = MainForm(request.POST)
        form1 = StepOneForm(request.POST)
        form2 = StepTwoForm(request.POST)
        form3 = StepThreeForm(request.POST)
        formset = StepFourFormSet(request.POST)

        if form0.is_valid():
            main = form0.save()

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
                KCFRESH_LOCATION_CODE = '00301'
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

            Product.getLossProductPercent(main)
            log(
                user=request.user,
                action="제품생산",
                obj=main,
                extra={
                    "ymd": main.ymd,
                    "total_loss_openEgg": float(main.total_loss_openEgg),
                    "total_loss_insert": float(main.total_loss_insert),
                    "total_loss_clean": float(main.total_loss_clean),
                    "total_loss_fill": float(main.total_loss_fill)
                }
            )
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


class ProductRecall(View):

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
        totalCount = ProductAdmin.objects.filter(product_id=product).values('product_id__code').annotate(
            totalCount=Sum(F('count')))
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
            # productAdmin = ProductAdmin.objects.filter(product_id=product).filter(releaseType='생성').first()
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
            return HttpResponse(status=400)


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
                      '제품생산',
                      '합계제품생산']
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        location = Location.objects.get(code='00301')
        egg = Egg.objects.values('code', 'codeName').filter(ymd__gte=start_date).filter(ymd__lte=end_date) \
            .filter(type='생산') \
            .annotate(report_egg_amount=ABS('amount')) \
            .annotate(report_egg_count=ABS('count')) \
            .annotate(report_sort_type=Value('원란', CharField())) \
            .annotate(report_rawTank_amount=Value(' ', CharField())) \
            .annotate(report_pastTank_amount=Value(' ', CharField())) \
            .annotate(report_product_amount=Value(' ', CharField())).order_by('codeName')

        total_amount = egg.aggregate(Sum('report_egg_amount'))['report_egg_amount__sum']
        total_count = egg.aggregate(Sum('report_egg_count'))['report_egg_count__sum']
        if not total_amount: total_amount = ' '
        if not total_count: total_count = ' '

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

        productAdmin = ProductAdmin.objects.values(code=F('product_id__code')) \
            .values(codeName=F('product_id__codeName')) \
            .filter(product_id__purchaseYmd=None) \
            .filter(ymd__gte=start_date).filter(ymd__lte=end_date) \
            .filter(location=location).filter(releaseType='이동').filter(count__lt=0) \
            .annotate(report_egg_amount=Value(' ', CharField())) \
            .annotate(report_egg_count=Value(' ', CharField())) \
            .annotate(report_sort_type=F('releaseType')) \
            .annotate(report_rawTank_amount=Value(' ', CharField())) \
            .annotate(report_pastTank_amount=Value(' ', CharField())) \
            .annotate(report_product_amount=F('amount')).order_by('codeName')

        total_rawTank = productEgg.filter(report_sort_type__in=['미출고품사용', '미출고품투입']) \
            .aggregate(Sum('report_rawTank_amount'))['report_rawTank_amount__sum']
        total_amount = product.filter(report_sort_type='미출고품사용') \
            .aggregate(Sum('report_product_amount'))['report_product_amount__sum']
        total_move_amount = productAdmin.filter(report_sort_type='이동') \
            .aggregate(Sum('report_product_amount'))['report_product_amount__sum']
        if total_move_amount: total_amount += total_move_amount
        if not total_rawTank: total_rawTank = ' '
        if not total_amount: total_amount = ' '
        total_other = [dict(code=' ',
                            codeName='합계',
                            report_sort_type='합계기타',
                            report_egg_amount=' ',
                            report_egg_count=' ',
                            report_rawTank_amount=total_rawTank,
                            report_pastTank_amount=' ',
                            report_product_amount=total_amount)]
        if total_other[0]['report_product_amount'] == ' ' and total_other[0]['report_rawTank_amount'] == ' ':
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
                  product,
                  total_product,
                  productAdmin),
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

                productAdmin = ProductAdmin.objects.create(  # TODO UPdate
                    product_id=product,
                    amount=count,
                    count=count,
                    ymd=ymd,
                    location=location,
                )
                product.save()
                productAdmin.save()

        return redirect('productList')

    def get(self, request):
        ProductOEMForm = ProductOEMFormSet(request.GET or None)
        return render(request, 'productOEM/productOEMReg.html', {'ProductOEMForm': ProductOEMForm})


class ProductOEMList(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'product.change_product'

    def get(self, request):
        productOEMForm = ProductOEMForm()
        return render(request, 'productOEM/productOEMList.html', {'productOEMForm': productOEMForm})
