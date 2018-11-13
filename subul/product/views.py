from django.db.models import Sum
from django.shortcuts import render
from django.views.generic.base import View
from core.models import Location
from product.models import ProductEgg, Product, ProductCode, ProductAdmin
from .forms import StepOneForm, StepTwoForm, StepThreeForm, StepFourForm, StepFourFormSet, MainForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class ProductRegister(LoginRequiredMixin, View):
    def post(self, request):
        form0 = MainForm(request.POST)
        form1 = StepOneForm(request.POST)
        form2 = StepTwoForm(request.POST)
        form3 = StepThreeForm(request.POST)
        formset = StepFourFormSet(request.POST)

        if form0.is_valid():
            main = form0.save()

        if form1.is_valid():
            print(form1.cleaned_data)
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

        if formset.is_valid():  # TODO formset vaild 찾아야됨
            for form in formset:
                code = form.cleaned_data.get('product')
                amount = form.cleaned_data.get('amount')
                amount_kg = form.cleaned_data.get('amount_kg')
                count = form.cleaned_data.get('count')
                memo = form.cleaned_data.get('memo')
                codeName = ProductCode.objects.filter(code=code)
                productExist = Product.objects.filter(code=code).filter(ymd=main.ymd).first()
                KCFRESH_LOCATION_CODE = '00301'
                location = Location.objects.get(code=KCFRESH_LOCATION_CODE)  # kcfresh 본사

                if amount_kg * count == amount:
                    print('############')
                    if not productExist:
                        product = Product.objects.create(
                            master_id=main,
                            ymd=main.ymd,
                            code=code,
                            codeName=codeName[0].codeName,
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
                        productExistAdmin = ProductAdmin.objects.filter(releaseType='생성')\
                                                                .filter(product_id=productExist).first()
                        productExistAdmin.amount += amount
                        productExistAdmin.count += count
                        productExist.save()
                        productExistAdmin.save()
            Product.getLossProductPercent(main)
        return render(request, 'product/productList.html')

    def get(self, request):
        tankValue = list(ProductEgg.objects.values('code', 'codeName').filter(delete_state='N')
                         .annotate(rawSum=Sum('rawTank_amount')).annotate(pastSum=Sum('pastTank_amount')).order_by(
            'code'))
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
    # login_url = '/'
    permission_required = 'articles.add_article'

    def get(self, request):
        return render(request, 'product/productList.html')
