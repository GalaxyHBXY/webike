from django.core.validators import MinValueValidator
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

    quantity = models.IntegerField(
        validators=[MinValueValidator(1)]
    )

    session_id = models.CharField(
        max_length=70
    )

    # This field can be changed as status
    has_paid = models.BooleanField(
        default=False,
        verbose_name='Payment Status'
    )

    has_shipped = models.BooleanField(
        default=False,
        verbose_name="Shipping"
    )

    created_on = models.DateTimeField(
        auto_now_add=True
    )

    updated_on = models.DateTimeField(
        auto_now_add=True
    )

    notes = models.CharField(
        default="",
        max_length=256,
        null=True,
        blank=True
    )

    class Mode(models.TextChoices):
        payment = ('PAYMENT','PAYMENT')
        subscription = ('SUBSCRIPTION','SUBSCRIPTION')

    mode = models.CharField(
        default=Mode.payment,
        max_length= 12
    )

    def __str__(self):
        return self.session_id
