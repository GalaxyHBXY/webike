from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

import user
# Create your views here.
from merchant.forms import CreateMerchantForm
from payments.models import OrderDetail
from user.forms import CreateUserForm

from product.models import Product
from user.views import signup
from .models import Merchant


@login_required
def home(request):
    merchant = Merchant.objects.get(user=request.user)
    context = {
        'products': Product.objects.filter(merchant=merchant).order_by("-id").filter(status=Product.Status.AVAILABLE),
        'merchant': merchant}
    orders = []
    for each in OrderDetail.objects.all():
        if each.product.merchant_id == merchant.pk:
            orders.append(each)
    context['orders'] = orders
    return render(request, template_name="merchant/merchant_homepage.html", context=context)


def merchant_signup(request):
    return signup(request,"Merchant")
