from django.urls import path

from .views import home, signup
from . import views

urlpatterns = [
    path('home', home, name='merchant_home'),
    path('signup', signup, name='merchant_signup')
]
