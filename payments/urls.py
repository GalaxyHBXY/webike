from django.urls import path
from .views import *

urlpatterns = [
    path('success/', PaymentSuccessView.as_view(), name='success'),
    path('failed/', PaymentFailedView.as_view(), name='failed'),
    path('api/checkout-session/<id>/', create_checkout_session, name='api_checkout_session'),
]