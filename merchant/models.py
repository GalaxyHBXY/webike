from django.db import models

# Create your models here.
from merchant import validators
from user.models import User


class Merchant(models.Model):
    class Meta:
        verbose_name = "Merchant"
        verbose_name_plural = "Merchants"

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name="merchant")

    abn_verified = models.BooleanField(default=False, null=False)
    abn = models.CharField(max_length=11,
                           unique=True,
                           null=True,
                           blank=True,
                           validators=[
                               validators.checkABN
                           ],
                           verbose_name='ABN')

    merchant_name = models.CharField(max_length=50,
                                     null=False,
                                     blank=False,
                                     verbose_name='Merchant Name')

    merchant_intro = models.CharField(max_length=250,
                                      null=True,
                                      blank=True,
                                      verbose_name='Merchant Introduction')

    def __str__(self):
        return self.merchant_name
