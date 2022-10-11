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
    stock = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    merchant = models.ForeignKey(Merchant, on_delete=models.DO_NOTHING, null=False, blank=False)
    description = models.CharField(max_length=255, null=False, blank=False)
    is_rent = models.BooleanField(default=False, verbose_name="This product is for rent")
    image = models.ImageField(null=False, blank=False, upload_to='media/product_pics', verbose_name='product_image',
                              validators=[validators.file_size_limit])
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    class Status(models.TextChoices):
        AVAILABLE = ('AVAILABLE', 'AVAILABLE')
        UNAVAILABLE = ('UNAVAILABLE', 'UNAVAILABLE')

    status = models.CharField(max_length=11, choices=Status.choices, default=Status.AVAILABLE, null=False,
                              blank=False, verbose_name="status")

    view_count = models.BigIntegerField(default = 0,
                                        blank=False,
                                        null=False,
                                        verbose_name="view count")

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

    class Brand(models.TextChoices):
        A = ('A', 'A')
        B = ('B', 'B')
        C = ('C', 'C')

    bike_brand = models.CharField(max_length=200, choices=Brand.choices, default=Brand.A, null=False, blank=False,
                                  verbose_name="Brand")
    # maybe need more choices for power/weight
    bike_power = models.CharField(max_length=200,  default=None, null=False, blank=False,
                                  verbose_name="Power")
    bike_weight = models.CharField(max_length=200,  default=None, null=False, blank=False,
                                  verbose_name="Weight")
    bike_longDescription = models.CharField(max_length=200,  null=False, blank=False,
                                  verbose_name="LongDescription")
