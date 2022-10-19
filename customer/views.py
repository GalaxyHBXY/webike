from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.shortcuts import render, redirect

import user
from customer.forms import CreateCustomerForm
from user.forms import CreateUserForm
from payments.models import OrderDetail
from user.views import signup


# Create your views here.


@login_required
def home(request):
    instance = request.user.customer
    personal_info = {'Email': request.user.email, 'Phone': request.user.phone}
    # Get all customer fields and values except for fields specified in exclude
    for key in model_to_dict(instance, exclude=['user', 'address']).keys():
        if hasattr(instance._meta.get_field(key), 'verbose_name'):
            personal_info[instance._meta.get_field(key).verbose_name] = getattr(instance, key)
        else:
            personal_info[key] = getattr(instance, key)

    # Add the formatted address
    personal_info['Residential Address'] = instance.address.formatted_address
    print(personal_info)
    context = {'orders': OrderDetail.objects.filter(customer=request.user).filter(has_paid=True),
               'personal_info': personal_info}
    return render(request, template_name="customer/customer_homepage.html", context=context)


def customer_signup(request):
    return signup(request, "Customer")
