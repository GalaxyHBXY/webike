from django.db import models

# Create your models here.
from user.models import User


class Customer(models.Model):
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name='customer')
    first_name = models.CharField(max_length=32,
                                  blank=False,
                                  null=False)
    last_name = models.CharField(max_length=32,
                                 blank=False,
                                 null=False)
