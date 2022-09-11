from django.urls import path

from customer.views import home,signup

urlpatterns = [
    path('home',home,name='customer_home'),
    path('signup',signup,name='customer_signup')


]
