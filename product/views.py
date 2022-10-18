import json

import requests
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from main.views import fail
from merchant.models import Merchant
from product.forms import createProductForm, createAddressForm, createBikeForm
from product.models import Product, Bike
from django.conf import settings
from payments.models import OrderDetail
from user.models import User


# Create your views here.
def add_new_product(request):
    context = {}

    # Validation
    if not request.user.is_authenticated:
        return redirect('index')

    if request.user.user_type != 'Merchant':
        return fail(request, "Permission Declined!")

    p_form = createProductForm()
    a_form = createAddressForm()

    # Pass GET data to context and override p_form to create bike
    if request.method == "GET":
        context['product_type'] = request.GET['product_type']

        if request.GET['product_type'] == "e_bike":
            p_form = createBikeForm()

    if request.method == 'POST':
        p_form = createProductForm(request.POST, request.FILES)
        a_form = createAddressForm(request.POST)

        if request.POST.get("product_type") == "e_bike":
            p_form = createBikeForm(request.POST, request.FILES)

        if p_form.is_valid() and a_form.is_valid():
            address_line1 = request.POST['address_line_1']
            suburb = request.POST['suburb']
            state = request.POST['state']

            API_KEY = 'AIzaSyA951Jowb33YxNfEoWnupBwVu6DXCISg3s'

            full_address = '{} {} {}'.format(address_line1, suburb, state)
            params = {
                'key': API_KEY,
                'address': full_address
            }
            base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
            response = requests.get(base_url, params=params).json()
            if response['status'] == 'OK':
                geometry = response['results'][0]['geometry']
                lat = geometry['location']['lat']
                lng = geometry['location']['lng']
                formatted_address = response['results'][0]['formatted_address']

                address = a_form.save(commit=False)
                address.lat = lat
                address.lng = lng
                address.formatted_address = formatted_address
                address.save()
            else:
                return fail(request, "Invalid network status")

            product = p_form.save(commit=False)

            # if request.POST.get("trade_type") == "sell":
            #     pass
            # else:
            #     pass

            product.merchant = request.user.merchant
            product.address = address
            product.save()
            return redirect("add_product_success")

    context['p_form'] = p_form
    context['a_form'] = a_form
    return render(request, template_name="product/add_product.html", context=context)


# This does not actually delete products from the database
# Instead it hides information from the users
# Reasons for this is that historical orders rely on product information
def delete_product(request):
    for p in Product.objects.filter(pk__in=request.POST.getlist("products")):
        p.status = Product.Status.UNAVAILABLE
        p.save()
    return redirect("merchant_home")


def success(request):
    return render(request, template_name="product/add_product_success.html")


def detail(request, id):
    product = None
    # checks if product exists and if yes checks if it is still available
    try:
        product = Product.objects.get(id=id)
        if product.status == Product.Status.UNAVAILABLE:
            raise ObjectDoesNotExist
    except ObjectDoesNotExist:
        return fail(request, "invalid request - product does not exist")

    is_bike = False
    user = request.user

    try:
        bike = Bike.objects.get(id=id)
        product = bike
        is_bike = True
    except ObjectDoesNotExist:
        pass

    # Add view count
    product.view_count += 1
    product.save()

    context = {'product': product,
               'is_bike': is_bike,
               'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
               'user': user
               }

    return render(request, template_name="product/product_detail.html", context=context)


def product_search(request):
    keyword = request.GET.get("keyword")
    result = []

    for each in Product.objects.filter(status=Product.Status.AVAILABLE):
        if keyword.lower() in each.get_product_all().lower():
            result.append(each)

    context = {"products": result}

    return render(request, template_name="product/product_search_result.html", context=context)


def product_filter(request):
    context = {}
    products = Bike.objects.filter(status=Bike.Status.AVAILABLE)

    size = [s.upper() for s in request.POST.getlist("size")]
    style = [s.upper() for s in request.POST.getlist("style")]
    brand = [s.upper() for s in request.POST.getlist("brand")]

    filters = [size, style, brand]

    # check if any of the filters is applied
    non_empty_flag = False
    for f in filters:
        if len(f) > 0:
            non_empty_flag = True

    if non_empty_flag:
        for f in filters:
            # if the filter is applied
            if f:
                products = products.intersection(Bike.objects.filter(bike_size__in=f))
    else:
        return render(request, template_name="product/product_search_result.html",
                      context={'products': Product.objects.filter(status=Product.Status.AVAILABLE)})

    context['products'] = products
    return render(request, template_name="product/product_search_result.html", context=context)


def find_corresponding_product(bike, Products):
    for each in Products:
        if bike.product_name == each.product_name:
            return each


def product_ship(request):
    order_id = json.loads(request.body)['order_id']
    try:
        order = OrderDetail.objects.get(pk=int(order_id))
        order.has_shipped = True
        order.save()
        return JsonResponse({"order_id": order_id, "status": "success"})
    except ObjectDoesNotExist:
        return JsonResponse({"order_id": order_id, "status": "failed"})
