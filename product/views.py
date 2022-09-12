import requests
from django.shortcuts import render, redirect

from main.views import fail
from merchant.models import Merchant
from product.forms import createProductForm, createAddressForm, createBikeForm
from product.models import Product
from django.conf import settings


# Create your views here.
def add_new_product(request):
    context = {}

    # Validation
    if not request.user.is_authenticated:
        return redirect('index')

    if request.user.user_type != 'Merchant':
        return fail(request, {"description": "Permission Declined!"})

    p_form = createProductForm()
    a_form = createAddressForm()

    # Pass GET data to context and override p_form to create bike
    if request.method == "GET":
        p_form = createBikeForm()
        context['trade_type'] = request.GET['trade_type']
        context['product_type'] = request.GET['product_type']

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

            if request.POST.get("trade_type") == "sell":
                pass
            else:
                pass

            product.merchant = request.user.merchant
            product.address = address
            product.save()
            return redirect("add_product_success")

    context['p_form'] = p_form
    context['a_form'] = a_form
    return render(request, template_name="product/add_product.html", context=context)


def success(request):
    return render(request, template_name="product/add_product_success.html")


def detail(request, id):
    product = Product.objects.get(id=id)
    context = {'product': product,
               'stripe_publishable_key':settings.STRIPE_PUBLISHABLE_KEY
               }
    return render(request, template_name="product/product_detail.html", context=context)


def product_search(request):
    keyword = request.GET.get("keyword")
    result = []

    for each in Product.objects.all():
        if keyword.lower() in each.get_product_all().lower():
            result.append(each)

    context = {"products": result}

    return render(request, template_name="product/product_search_result.html", context=context)

    # print(keyword)


def product_filter(request):
    low_price = request.GET.get("low_price")
    high_price = request.GET.get("high_price")

    location = request.GET.get("location")
    bike_size = request.GET.get("bike_size")
    style = request.GET.get("style")

    products = Product.objects.all()

    if low_price is not None and high_price is not None:
        low_price = float(low_price)
        high_price = float(high_price)
        if high_price >= low_price >= 0:
            products = products.filter(price__range=(low_price, high_price))
        else:
            return fail(request, {"description": "Invalid price range"})

    products = products.filter(address__formatted_address__icontains=location)

    context = {"products": products}

    return render(request, template_name="product/product_search_result.html", context=context)

    # if bike_size!=None:
    #     pass

    # if style!=None:
    #     pass

    pass
