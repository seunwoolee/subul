from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.test import TestCase
from django.urls import reverse, resolve

from users.models import CustomUser
from users.views import CustomLoginView


class UserTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user: CustomUser = get_user_model()
        cls.user_data: dict = {'username': 'testuser', 'password': 'testuser'}

    def setUp(self):
        url = reverse('login')
        self.testuser = self.user.objects.create_user(**self.user_data)
        self.response = self.client.get(url)

    def test_login_form_check(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, AuthenticationForm)
        self.assertTemplateUsed(self.response, 'registration/login.html')
        self.assertContains(self.response, 'Login')

    def test_login_success(self):
        response = self.client.post(reverse('login'), self.user_data)
        self.assertEqual(response.status_code, 302)

    def test_login_fail(self):
        user_data: dict = {'username': 'testuser', 'password': 'tetuser'}
        response = self.client.post(reverse('login'), user_data)
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        view = resolve('/accounts/login/')
        self.assertEqual(view.func.__name__, CustomLoginView.as_view().__name__)
