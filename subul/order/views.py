from django.shortcuts import render
from django.views import View

from order.forms import OrderFormSet


class OrderList(View):
    def get(self, request):
        return render(request, 'order/orderList.html')

class OrderReg(View):
        # def post(self, request):
        #     form0 = MainForm(request.POST)
        #     form1 = StepOneForm(request.POST)
        #     form2 = StepTwoForm(request.POST)
        #     form3 = StepThreeForm(request.POST)
        #     formset = StepFourFormSet(request.POST)
        #
        #     if form0.is_valid():
        #         main = form0.save()
        #
        #     if form1.is_valid():
        #         print(form1.cleaned_data)
        #         stepOneProductEgg = [[key, value] for key, value in form1.cleaned_data.items()]
        #         memo = [stepOneProductEgg[i][1] for i in range(2, len(stepOneProductEgg), 3)]  # 메모만 가져오기
        #         validStepOne = ProductEgg.makeVaildinfo(stepOneProductEgg, memo)
        #         ProductEgg.insertInfo(main, validStepOne)
        #         ProductEgg.getLossOpenEggPercent(main)
        #
        #     if form2.is_valid():
        #         stepTwoProductEgg = [[key, value] for key, value in form2.cleaned_data.items()]
        #         memo = [stepTwoProductEgg[i][1] for i in range(1, len(stepTwoProductEgg), 2)]
        #         validStepTwo = ProductEgg.makeVaildinfo(stepTwoProductEgg, memo)
        #         ProductEgg.insertInfo(main, validStepTwo)
        #
        #     if form3.is_valid():
        #         stepThreeProductEgg = [[key, value] for key, value in form3.cleaned_data.items()]
        #         memo = [stepThreeProductEgg[i][1] for i in range(1, len(stepThreeProductEgg), 2)]
        #         validStepThree = ProductEgg.makeVaildinfo(stepThreeProductEgg, memo)
        #         ProductEgg.insertInfo(main, validStepThree)
        #
        #     if formset.is_valid():  # TODO formset vaild 찾아야됨
        #         for form in formset:
        #             code = form.cleaned_data.get('product')
        #             amount = form.cleaned_data.get('amount')
        #             count = form.cleaned_data.get('count')
        #             memo = form.cleaned_data.get('memo')
        #             codeName = ProductCode.objects.filter(code=code)
        #             try:
        #                 product = Product.objects.create(
        #                     master_id=main,
        #                     ymd=main.ymd,
        #                     code=code,
        #                     codeName=codeName[0].codeName,
        #                     amount=amount,
        #                     count=count,
        #                     memo=memo
        #                 )
        #                 # ProductAdmin도 insert 해줘야...
        #                 location = Location.objects.get(code=301)
        #                 productAdmin = ProductAdmin.objects.create(
        #                     product_id=product,
        #                     amount=amount,
        #                     count=count,
        #                     ymd=main.ymd,
        #                     location=location,
        #                 )
        #                 product.save()
        #                 productAdmin.save()
        #             except:
        #                 pass
        #         Product.getLossProductPercent(main)  # 수율
        #     return render(request, 'product/productRegister.html')

        def get(self, request):
            orderForm = OrderFormSet(request.GET or None)
            return render(request, 'order/orderReg.html', {'orderForm': orderForm})
