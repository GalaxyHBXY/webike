from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Create your views here.
import user
from customer.forms import CreateCustomerForm
from main.views import fail
from merchant.forms import CreateMerchantForm
from product.forms import createAddressForm
from product.views import get_formatted_address
from utils.GmailAPI import gmail_send_message
from user.forms import CreateUserForm

from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

from user.models import User


def user_login(request):
    context = {"msg": ""}
    if request.method == 'POST':
        email = request.POST.get('login_email')
        password = request.POST.get('login_password')
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            if user.status == 'Normal':
                # return
                login(request, user)
                # if Employer.objects.filter(user=request.user).exists():
                #     return redirect('../employer/empl_home')
                print(user.user_type)
                if user.user_type == 'Customer':
                    return redirect('customer_home')
                else:
                    return redirect('merchant_home')

            else:
                context['msg'] = 'This account is blocked, please contact the website admin.'
        else:
            context['msg'] = 'Incorrect username/password or account not verified.'
    return render(request, 'user/login.html', context)


def user_logout(request):
    logout(request)
    return redirect("index")


def user_signup(request):
    return render(request, 'user/signup.html')


def reset_password(request):
    return render(request, 'user/reset_password.html')


def signup_successful(request):
    return render(request, template_name="user/signup_successful.html")


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(email=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def signup(request, user_type):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        u_form = CreateUserForm()
        t_form = None
        a_form = None
        template_name = None

        if user_type == "Customer":
            t_form = CreateCustomerForm()
            a_form = createAddressForm()
            template_name = "customer/customer_signup_page.html"
        else:
            t_form = CreateMerchantForm()
            template_name = "merchant/merchant_signup_page.html"

        if request.method == 'POST':
            u_form = CreateUserForm(request.POST)
            user = None
            valid_flag = False
            if user_type == "Customer":
                t_form = CreateCustomerForm(request.POST)
                a_form = createAddressForm(request.POST)
                if u_form.is_valid() and t_form.is_valid() and a_form.is_valid():
                    valid_flag = True
                    gmap_response = get_formatted_address(request.POST['address_line_1'],
                                                          request.POST['suburb'],
                                                          request.POST['state'])
                    if gmap_response:
                        address = a_form.save(commit=False)
                        address.lat = gmap_response[0]
                        address.lng = gmap_response[1]
                        address.formatted_address = gmap_response[2]
                        address.save()
                    else:
                        return fail(request, "Invalid network status")

                    user = u_form.save(commit=False)
                    user.user_type = user_type
                    user.is_active = False
                    user.save()

                    customer = t_form.save(commit=False)
                    customer.user = user
                    customer.address = a_form.save(commit=False)
                    customer.save()
            else:
                t_form = CreateMerchantForm(request.POST)
                if u_form.is_valid() and t_form.is_valid():
                    valid_flag = True
                    user = u_form.save(commit=False)
                    user.user_type = user_type
                    user.is_active = False
                    user.save()

                    t_form = CreateMerchantForm(request.POST)
                    merchant = t_form.save(commit=False)
                    merchant.user = user
                    merchant.save()

            if valid_flag:
                # send verification email
                message = render_to_string('utils/email/acc_active_email.html', {
                    'user': user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.email)),
                    'token': account_activation_token.make_token(user),
                })
                gmail_send_message(user.email, "【WeBike】Activate your account.", message)

                return redirect('signup_successful')

    context = {'u_form': u_form, 't_form': t_form, 'a_form': a_form}
    return render(request, template_name=template_name, context=context)
