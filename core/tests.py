from django.test import TestCase

from core.models import OrderTime
from users.models import CustomUser


class CoreTest(TestCase):
    def test_order_time(self):
        user = CustomUser.objects.create(username="컬리")
        user.set_password("asdf")
        user.first_name = '컬리'
        user.last_name = '업체'
        order_time = OrderTime.objects.create(
            user,
            0,
            2358
        )
        self.assertEqual(order_time.end, 2358)
