from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Customer
from user.models import User
from django.urls import reverse
from .views import home


# Create your tests here.
class CustomerTestCase(TestCase):
    def setUp(self):
        # customer user with user_type as customer
        self.customer_email = "testCustomer@gmail.com"
        self.customer_phone = "000123"
        self.customer_user_type = "Customer"
        self.customer_status = "Normal"
        self.customer_pw = "Password123"

        self.user = User()
        # self.customer.email = self.customer_email
        # self.customer.phone = self.customer_phone
        # self.customer.user_type = self.customer_user_type
        # self.customer.status = self.customer_status
        # self.customer.set_password(self.customer_pw)
        # self.customer.save()
        self.customer = Customer(user=self.user, first_name="first_name", last_name="last_name")

        self.client = Client()

    def test_customer_model(self):
        self.assertEqual(self.customer.first_name, "first_name")

    def test_signup(self):
        self.client.post('/customer/signup', {
            'email': 'test1@email.com',
            'password1': 'pavlodar',
            'password2': 'pavlodar',
            'phone': 'Mypassword777',
            'first_name': 'first',
            'last_name': 'last'
        })
        self.assertFalse(Customer.objects.filter(first_name='first').exists())
