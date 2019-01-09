from django.db.models import Sum, F
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from rest_framework import status
from rest_framework.response import Response

from core.models import Location
from eventlog.models import log
from product.models import ProductEgg, Product, ProductCode, ProductAdmin, ProductMaster
from .forms import StepOneForm, StepTwoForm, StepThreeForm, StepFourForm, StepFourFormSet, MainForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class ProductRegister(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/'
    permission_required = 'product.add_product'

    def post(self, request):
        form0 = MainForm(request.POST)
        form1 = StepOneForm(request.POST)
        form2 = StepTwoForm(request.POST)
        form3 = StepThreeForm(request.POST)
        formset = StepFourFormSet(request.POST)

        if form0.is_valid():
            ymd = form0.cleaned_data.get('ymd', None)
            productMaster = ProductMaster.objects.filter(ymd=ymd).first()

            if productMaster:
                main = productMaster
            else:
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

                if code and amount and amount_kg and count:
                    productCode = ProductCode.objects.get(code=code)
                    productExist = Product.objects.filter(code=code).filter(ymd=main.ymd).first()
                    if amount_kg * count == amount:
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
                            productExist.amount += amount
                            productExist.count += count
                            productExistAdmin = ProductAdmin.objects.filter(releaseType='생성') \
                                .filter(product_id=productExist).first()
                            productExistAdmin.amount += amount
                            productExistAdmin.count += count
                            productExist.save()
                            productExistAdmin.save()

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
    login_url = '/'
    permission_required = 'product.change_product'

    def get(self, request):
        # product = Product.objects.first()
        # log(
        #     user=request.user,
        #     action="가나다라마",
        #     obj=product,
        #     extra={
        #         "name":product.codeName,
        #         "amount":product.amount
        #     }
        # )
        return render(request, 'product/productList.html')


class ProductRecall(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/'
    permission_required = 'product.change_product'

    def post(self, request, pk):
        CODE_TYPE_CHOICES = {
            '01201': 'RAW Tank 전란',
            '01202': 'RAW Tank 난황',
            '01203': 'RAW Tank 난백',
        }
        ymd = request.POST['ymd']
        amount = int(request.POST['amount'])
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