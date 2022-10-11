from django.contrib import admin

from product.models import Product, Address, Bike


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'merchant')


class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'lng', 'lat', 'state', 'formatted_address')
    ordering = ('id',)


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Bike)
