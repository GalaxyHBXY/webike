from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.
from merchant.forms import CreateMerchantForm
from payments.models import OrderDetail
from user.forms import CreateUserForm

from product.models import Product
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


def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        u_form = CreateUserForm()
        m_form = CreateMerchantForm()
        if request.method == 'POST':
            u_form = CreateUserForm(request.POST)
            m_form = CreateMerchantForm(request.POST)
            if u_form.is_valid() and m_form.is_valid():
                user = u_form.save(commit=False)
                user.user_type = 'Merchant'
                user.save()
                merchant = m_form.save(commit=False)
                merchant.user = user
                merchant.save()

                # send_ver_email(user, request)
                login(request, user)
                return redirect('merchant_home')
    context = {'u_form': u_form, 'm_form': m_form}
    return render(request, template_name="merchant/merchant_signup_page.html", context=context)
