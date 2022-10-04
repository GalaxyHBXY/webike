from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from customer.forms import CreateCustomerForm
from user.forms import CreateUserForm
from payments.models import OrderDetail


# Create your views here.


@login_required
def home(request):
    context = {'orders': OrderDetail.objects.filter(customer=request.user)}
    return render(request, template_name="customer/customer_homepage.html", context=context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        u_form = CreateUserForm()
        c_form = CreateCustomerForm()
        if request.method == 'POST':
            u_form = CreateUserForm(request.POST)
            c_form = CreateCustomerForm(request.POST)
            if u_form.is_valid() and c_form.is_valid():
                user = u_form.save(commit=False)
                user.user_type = 'Customer'
                user.save()
                customer = c_form.save(commit=False)
                customer.user = user
                customer.save()

                # send_ver_email(user, request)
                login(request, user)
                return redirect('customer_home')

        context = {'u_form': u_form, 'c_form': c_form}
        return render(request, template_name="customer/customer_signup_page.html", context=context)
