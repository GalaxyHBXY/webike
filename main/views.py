from django.shortcuts import render

from product.models import Product


# Create your views here.
def index(request):
    return render(request, template_name="main/index.html",
                  context={'hide_hr': True,
                           'products': Product.objects.filter(status=Product.Status.AVAILABLE).order_by("-view_count")[:6]})


def webikers(request):
    return render(request, template_name="main/webikers.html")


def wesellers(request):
    return render(request, template_name="main/wesellers.html")


def werenters(request):
    return render(request, template_name="main/werenters.html")


def fail(request, description):
    return render(request, "main/fail.html", context={"description": description})
