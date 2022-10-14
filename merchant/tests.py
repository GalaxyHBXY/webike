import os
from unittest import mock
import json
from django.conf import settings
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from product.forms import createProductForm, createAddressForm
from product.models import Product, Address
from user.models import User
from merchant.models import Merchant


# Create your tests here.
class MerchantTestCase(TestCase):
    def setUp(self):
        self.user = User()
        self.merchant = Merchant(user=self.user, abn_verified=True, abn='123', merchant_name='name',
                                 merchant_intro='info')
        self.client = Client()

    def test_merhchant_model(self):
        self.assertEqual(self.merchant.abn, "123")

    def test_sign_up(self):
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
        self.assertFalse(Merchant.objects.filter(abn='123').exists())

    def test_upload_project(self):
        # signup
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
        self.assertFalse(Merchant.objects.filter(abn='123').exists())
        # login first
        login_url = "/login"
        self.assertEqual(settings.LOGIN_URL, login_url)
        data = {"login_email": 'test1@email.com', "login_password": 'pavlodar'}
        response = self.client.post(login_url, data, follow=True)
        status_code = response.status_code
        redirect_path = response.request.get("PATH_INFO")
        print("now we are" + redirect_path)
        self.assertEqual(reverse("merchant_home"), redirect_path)
        self.assertEqual(status_code, 200)
        print("before")
        print(Product.objects.all().count())
        # p_form = ['name',100,100,'a brief one',mock.MagicMock(spec=File, name='FileMock')]
        # a_form = ['address line one','redforn','NSW',2020]
        # data = {
        #     "product_type": 'accessories',
        #     'product_name': 'name',
        #     'price': 100.0,
        #     'stock': 100,
        #     'status': 'AVAILABLE',
        #     'view_count': 1,
        #     'is_rent': False,
        #     'description': 'a brief one',
        #     'image': 'media/product_pics/fireball.png',
        #     'address_line_1': '1',
        #     'suburb': 'redforn',
        #     'state': 'NSW',
        #     'postcode': 2020
        # }
        #
        # a_form = createAddressForm({
        #     'address_line_1': '1',
        #     'suburb': 'redforn',
        #     'state': 'NSW',
        #     'postcode': 2020
        # })
        #
        # address = a_form.save()
        #
        # file_mock = mock.MagicMock(spec=File, name='FileMock')
        # self.image = file_mock
        # upload_file = open('media/media/product_pics/fireball.png', 'rb')
        # form = createProductForm(
        #     data={
        #         'product_name': 'name',
        #         'price': 100.0,
        #         'stock': 100,
        #         'description': 'a brief one',
        #     },
        #     files={'image': SimpleUploadedFile(upload_file.name, upload_file.read())}
        # )

        # self.client.post()
        # print(form.is_valid())
        # print(form.errors)
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
            print(response.status_code)
            print("after")
            print(Product.objects.all().count())

