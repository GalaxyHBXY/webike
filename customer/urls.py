from django.urls import path

from customer.views import home,customer_signup

urlpatterns = [
    path('home',home,name='customer_home'),
    path('signup',customer_signup,name='customer_signup')
]
