from django.shortcuts import render

from product.models import Product


# Create your views here.
def index(request):
    return render(request, template_name="main/index.html", context={'hide_hr': True, 'products': Product.objects.order_by("-id")})


def fail(request, context):
    return render(request, "main/fail.html", context=context)
