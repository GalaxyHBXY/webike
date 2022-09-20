from django.core.validators import MinValueValidator
from django.db import models

from merchant.models import Merchant
from product import validators


# Create your models here.

class Address(models.Model):
    address_line_1 = models.CharField(max_length=255, default="", null=False, blank=False,
                                      verbose_name="address_line_1", help_text="460 Jones St")
    suburb = models.CharField(max_length=20,
                              default="",
                              null=False,
                              blank=False,
                              verbose_name='Suburb',
                              help_text='e.g. Chatswood')
    postcode = models.CharField(max_length=4,
                                default="",
                                null=False,
                                blank=False,
                                verbose_name='Post Code',
                                help_text='e.g. 2017')
    lng = models.DecimalField(max_digits=9, decimal_places=6, default=0.00)
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=0.00)
    formatted_address = models.CharField(max_length=255, default="", verbose_name="Official Address")

    class State(models.TextChoices):
        NSW = ('NSW', 'NSW')
        VIC = ('VIC', 'VIC')
        QLD = ('QLD', 'QLD')
        WA = ('WA', 'WA')
        SA = ('SA', 'SA')
        TAS = ('TAS', 'TAS')
        ACT = ('ACT', 'ACT')
        NT = ('NT', 'NT')

    state = models.CharField(max_length=3,
                             choices=State.choices,
                             default=State.NSW,
                             null=False,
                             blank=False,
                             verbose_name='State')

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self) -> str:
        return self.formatted_address


class Product(models.Model):
    product_name = models.CharField(max_length=255, null=False, blank=False)
    price = models.FloatField(default=0, validators=[MinValueValidator(0)])
    merchant = models.ForeignKey(Merchant, on_delete=models.DO_NOTHING, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    image = models.ImageField(null=False, blank=False, upload_to='media/product_pics', verbose_name='product_image',
                              validators=[validators.file_size_limit])

    class Status(models.TextChoices):
        AVALIABLE = ('AVALIABLE', 'AVALIABLE')
        UNAVAIABLE = ('UNAVALIABLE', 'UNAVALIABLE')

    status = models.CharField(max_length=11, choices=Status.choices, default=Status.AVALIABLE, null=False,
                              blank=False, verbose_name="status")
    stock = models.IntegerField(default=1, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.product_name

    def get_product_all(self):
        return "{} {} {} {} {}".format(self.product_name, self.price, self.merchant, self.description, self.address)


class Bike(Product):
    class BikeSize(models.TextChoices):
        SMALL = ('SMALL', 'SMALL')
        MEDIUM = ('MEDIUM', 'MEDIUM')
        LARGE = ('LARGE', 'LARGE')

    bike_size = models.CharField(max_length=6, choices=BikeSize.choices, default=BikeSize.SMALL, null=False,
                                 blank=False, verbose_name="BikeSize")

    class Style(models.TextChoices):
        STYLEA = ('STYLEA', 'STYLEA')
        STYLEB = ('STYLEB', 'STYLEB')
        STYLEC = ('STYLEC', 'STYLEC')

    bike_style = models.CharField(max_length=200, choices=Style.choices, default=Style.STYLEA, null=False, blank=False,
                                  verbose_name="Style")

    is_rent = models.BooleanField(default=False, verbose_name="This product is for rent")

