from django.db import models

from product.models import Address
# Create your models here.
from user.models import User


class Customer(models.Model):
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name="customer")
    first_name = models.CharField(max_length=32,
                                  blank=False,
                                  null=False,
                                  verbose_name="Fist Name")
    last_name = models.CharField(max_length=32,
                                 blank=False,
                                 null=False,
                                 verbose_name="Last Name")
    address = models.OneToOneField(Address,
                                   on_delete=models.CASCADE,
                                   blank=False,
                                   null=False,
                                   verbose_name="Residential Address")

    class EmergencyContact(models.TextChoices):
        Partner = ('Partner', 'Partner')
        Relative = ('Relative', 'Relative')
        Friend = ('Friend', 'Friend')
        Colleague = ('Colleague', 'Colleague')

    emergency_contact = models.CharField(max_length=11,
                                         choices=EmergencyContact.choices,
                                         default=EmergencyContact.Relative,
                                         blank=False,
                                         null=False,
                                         verbose_name="Emergency Contact Relationship",
                                         help_text="Please choose your relationship with this emergency contact person")

    emergency_contact_phone = models.CharField(max_length=15,
                                               blank=False,
                                               null=False,
                                               default="",
                                               verbose_name="Emergency Contact Number")
