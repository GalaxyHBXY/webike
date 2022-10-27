from django.test import TestCase
from django.test.client import RequestFactory

from payments.views import get_created_checkout_session, cancel_subscription, create_checkout_session


# Create your tests here.
class PaymentTestCase(TestCase):
    def test_details(self):
        rf = RequestFactory()
