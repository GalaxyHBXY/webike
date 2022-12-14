"""webike URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from main.views import index, wesellers, werenters, webikers
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from user.views import user_login, user_logout, user_signup, reset_password, activate, signup_successful
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('main/', include('main.urls')),
    path('user/', include('user.urls')),
    path('login', user_login, name='login'),
    path('signup', user_signup, name='signup'),
    path('logout', user_logout, name='logout'),
    path('customer/', include('customer.urls')),
    path('merchant/', include('merchant.urls')),
    path('product/', include('product.urls')),
    path('reset_password/', reset_password, name="reset_password"),
    path('pay', include('payments.urls')),
    path('webikers', webikers, name="webikers"),
    path('wesellers', wesellers, name="wesellers"),
    path('werenters', werenters, name="werenters"),
    path('signup/successful', signup_successful, name='signup_successful'),
    path('activate/<uidb64>/<token>', activate, name='activate')
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
