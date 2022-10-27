from django.test import TestCase
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse

User = get_user_model()


# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        # customer user with user_type as customer
        self.customer_email = "testCustomer@gmail.com"
        self.customer_phone = "000123"
        self.customer_user_type = "Customer"
        self.customer_status = "Normal"
        self.customer_pw = "Password123"

        self.customer = User()
        self.customer.email = self.customer_email
        self.customer.phone = self.customer_phone
        self.customer.user_type = self.customer_user_type
        self.customer.status = self.customer_status
        self.customer.set_password(self.customer_pw)
        self.customer.save()

        # customer user with user_type as merchant
        self.merchant_email = "testMerchant@gmail.com"
        self.merchant_phone = "000456"
        self.merchant_user_type = "Merchant"
        self.merchant_status = "Normal"
        self.merchant_pw = "admin"

        self.merchant = User()
        self.merchant.email = self.merchant_email
        self.merchant.phone = self.merchant_phone
        self.merchant.user_type = self.merchant_user_type
        self.merchant.status = self.merchant_status
        self.merchant.set_password(self.merchant_pw)
        self.merchant.save()

    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 2)

    def test_user_password(self):
        self.assertTrue(self.customer.check_password(self.customer_pw))
        self.assertFalse(self.merchant.check_password("randomPassword"))

    def test_login_url(self):
        login_url = "/login"
        self.assertEqual(settings.LOGIN_URL, login_url)
        data = {"login_email": self.customer_email, "login_password": self.customer_pw}
        # response = self.client.post(login_url, data, follow=True)
        # status_code = response.status_code
        # redirect_path = response.request.get("PATH_INFO")
        # self.assertEqual(redirect_path, reverse("customer_home"))
        # self.assertEqual(status_code, 200)
