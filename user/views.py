from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.
import user


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
