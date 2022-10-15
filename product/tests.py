from django.conf import settings
from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse

from merchant.models import Merchant
from product.models import Product
from user.models import User


class ProductTestCase(TestCase):
    def setUp(self):
        self.user = User()
        self.merchant = Merchant(user=self.user, abn_verified=True, abn='123', merchant_name='name',
                                 merchant_intro='info')
        self.client = Client()
        # registration
        self.client.post('/merchant/signup', {
            'email': 'test1@email.com',
            'password1': 'pavlodar',
            'password2': 'pavlodar',
            'phone': 'Mypassword777',
            'abn_verified': True,
            'abn': '123',
            'merchant_name': 'name',
            'merchant_intro': 'info'
        })

        # login
        login_url = "/login"
        data = {"login_email": 'test1@email.com', "login_password": 'pavlodar'}
        response = self.client.post(login_url, data, follow=True)


    def test_merchant_upload_product(self):
        counts_before_upload = Product.objects.all().count()
        with open('media/media/product_pics/fireball.png', 'rb') as upload_file:
            response = self.client.post(
                "/product/add_new_product",
                data={
                    'product_name': 'name',
                    'price': 100.0,
                    'stock': 100,
                    'description': 'a brief one',
                    'image': upload_file,
                    'address_line_1': '1',
                    'suburb': 'redforn',
                    'state': 'NSW',
                    'postcode': 2020
                }
            )
        counts_after_upload = Product.objects.all().count()
        self.assertEqual(counts_after_upload,counts_before_upload+1)
