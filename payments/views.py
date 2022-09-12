import requests
from django.http.response import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse



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

    stripe.api_key = settings.STRIPE_SECRET_KEY
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
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('success')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('failed')),
    )

    order = OrderDetail()
    order.customer = request.user
    order.product = product
    order.stripe_payment_intent = checkout_session['payment_intent']
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

        order = get_object_or_404(OrderDetail, stripe_payment_intent=session.payment_intent)
        # if not order.has_paid:
        #     current_user = request.user
        #     product = order.product
        #     current_user.credit_coin += product.price
        #     current_user.free_coin += product.gift
        #     current_user.save()
        #     order.has_paid = True
        #     order.save()

        return render(request, self.template_name)


class PaymentFailedView(LoginRequiredMixin, TemplateView):
    template_name = "payments/payment_failed.html"
