from django.test import TestCase, Client
from user.models import User
from merchant.models import Merchant


# Create your tests here.
class MerchantTestCase(TestCase):
    def setUp(self):
        self.user = User()
        self.merchant = Merchant(user=self.user, abn_verified=True, abn='123', merchant_name='name', merchant_intro='info')
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
