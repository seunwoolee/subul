from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework.test import APIClient

from core.models import Location
from eventlog.models import Log
from order.models import Order
from product.models import ProductCode
from users.models import CustomUser
from users.views import CustomLoginView


class OrderTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user: CustomUser = get_user_model()

        cls.user_data: dict = {'username': 'testuser', 'password': 'testuser'}
        cls.testuser = cls.user.objects.create_user(**cls.user_data)

        cls.productCode_data: dict = \
            {'code': '00000', 'codeName': '맛있는계란', 'type': '전란', 'amount_kg': 0.50, 'price': 1000}
        cls.productCode = ProductCode(**cls.productCode_data)
        cls.productCode.save()

        cls.location_data: dict = \
            {'code': '00000', 'codeName': '전산팀', 'type': '판매', 'location_manager': cls.testuser}
        cls.location = Location(**cls.location_data)
        cls.location.save()

        cls.order_data = \
            {'ymd': '20191230', 'count': 2, 'amount': 1.00, 'memo': 'test',
             'productCode': cls.productCode, 'orderLocationCode': cls.location,
             'orderLocationName': cls.location.codeName, 'type': '판매'}
        cls.order_data: dict = dict(cls.productCode_data, **cls.order_data)
        cls.order = Order(**cls.order_data)
        cls.order.save()

    def setUp(self):
        self.client = APIClient()
        self.login_response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testuser'
        })
        self.assertEqual(self.login_response.status_code, 302)

    def test_order_model_data_check(self):
        self.assertEqual(1, self.order.id)
        self.assertEqual('00000', self.order.code)
        self.assertEqual('맛있는계란', self.order.codeName)
        self.assertEqual(0.50, self.order.amount_kg)
        self.assertEqual(1000, self.order.price)

    def test_order_update(self):
        url = '/api/order/' + str(self.order.id)
        response = self.client.patch(url, data=self.order_data)
        self.assertEqual(response.status_code, 200)

        log = Log.objects.first()
        self.assertEqual(log.object_id, self.order.id)
        self.assertEqual(log.action, '주문수정')

    def test_order_delete(self):
        url = '/api/order/' + str(self.order.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

        log = Log.objects.first()
        self.assertEqual(log.object_id, self.order.id)
        self.assertEqual(log.action, '주문삭제')
