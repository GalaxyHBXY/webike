from django.urls import path

from .views import home,merchant_signup

urlpatterns = [
    path('home', home, name='merchant_home'),
    path('signup', merchant_signup, name='merchant_signup')
]
