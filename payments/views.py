import requests
from django.http.response import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from main.views import fail
from product.models import Bike
from .models import *
from django.views.generic import TemplateView
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

# Create your views here.
@csrf_exempt
def create_checkout_session(request, id):
    request_data = json.loads(request.body)
    product = get_object_or_404(Product, pk=id)

    quantity = request_data['quantity']
    # 有被篡改

    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = None

    if int(product.stock) < int(quantity) or quantity == 0:
        return fail(request, "Insufficient product stock")
    if product.is_rent:
        checkout_session = get_created_checkout_session(request, request_data, quantity, product, mode="subscription")
    else:
        checkout_session = get_created_checkout_session(request, request_data, quantity, product, mode="payment")

    order = OrderDetail()
    order.customer = request.user
    order.product = product
    order.quantity = quantity
    order.session_id = checkout_session.stripe_id
    # print(checkout_session.id)
    # order.mode = mode.upper()
    order.save()

    return JsonResponse({'sessionId': checkout_session.id})


class PaymentSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "payments/payment_success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        order = get_object_or_404(OrderDetail, session_id=session.stripe_id)

        order.product.stock = order.product.stock - order.quantity
        order.has_paid = True
        order.product.save()
        order.save()

        return render(request, self.template_name)


class PaymentFailedView(LoginRequiredMixin, TemplateView):
    template_name = "payments/payment_failed.html"


def get_created_checkout_session(request, request_data, quantity, product, mode):
    if (mode == "subscription"):
        checkout_session = stripe.checkout.Session.create(
            # Customer Email is optional,
            # It is not safe to accept email directly from the client side
            customer_email=request_data['email'],
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'aud',
                        'product_data': {
                            'name': product.product_name,
                        },
                        "recurring": {"interval": "week"},
                        'unit_amount': int(product.price * 100),

                    },

                    'quantity': quantity,
                }
            ],

            mode=mode,
            success_url=request.build_absolute_uri(
                reverse('success')
            ) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('failed')),
        )
    else:
        checkout_session = stripe.checkout.Session.create(
            # Customer Email is optional,
            # It is not safe to accept email directly from the client side
            customer_email=request_data['email'],
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'aud',
                        'product_data': {
                            'name': product.product_name,
                        },
                        'unit_amount': int(product.price * 100),

                    },

                    'quantity': quantity,
                }
            ],

            mode=mode,
            success_url=request.build_absolute_uri(
                reverse('success')
            ) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('failed')),
        )

    return checkout_session


def cancel_subscription(request, id):
    order = OrderDetail.objects.filter(pk=id)
    if (len(order) != 1):
        return fail("subscription does not exist")

    stripe.api_key = settings.STRIPE_SECRET_KEY
    order = order[0]
    print('')
    print(order.session_id)
    print(stripe.checkout.Session.retrieve(order.session_id))
    print('')

    try:
        subscription_id = stripe.checkout.Session.retrieve(order.session_id)["subscription"]
        stripe.Subscription.delete(subscription_id)
    except:
        return render(request, template_name="payments/order_cancel_failed.html")

    order.product.is_rent = False
    order.save()
    print(order.product.is_rent)

    return render(request, template_name="payments/order_cancel_success.html")
