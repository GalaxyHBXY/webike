from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

import user
from customer.forms import CreateCustomerForm
from user.forms import CreateUserForm
from payments.models import OrderDetail
from user.views import signup


# Create your views here.


@login_required
def home(request):
    context = {'orders': OrderDetail.objects.filter(customer=request.user).filter(has_paid=True)}
    return render(request, template_name="customer/customer_homepage.html", context=context)


def customer_signup(request):
    return signup(request,"Customer")
