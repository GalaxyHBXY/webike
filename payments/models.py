from django.db import models

from product.models import Product
from user.models import User


# Create your models here.

class OrderDetail(models.Model):

    id = models.BigAutoField(
        primary_key=True
    )

    customer = models.ForeignKey(
        to=User,
        verbose_name='Customer Email',
        on_delete=models.PROTECT,
        default=None
    )

    product = models.ForeignKey(
        to=Product,
        verbose_name='Product',
        on_delete=models.PROTECT
    )

    stripe_payment_intent = models.CharField(
        max_length=200
    )

    # This field can be changed as status
    has_paid = models.BooleanField(
        default=False,
        verbose_name='Payment Status'
    )

    created_on = models.DateTimeField(
        auto_now_add=True
    )

    updated_on = models.DateTimeField(
        auto_now_add=True
    )

    notes = models.CharField(
        default="",
        max_length=256
    )

    def __str__(self):
        return self.stripe_payment_intent
