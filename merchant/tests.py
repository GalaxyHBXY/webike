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


