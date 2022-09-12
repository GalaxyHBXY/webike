from django.contrib import admin
from .models import *


class OrderDetails_Admin(admin.ModelAdmin):
    list_display=('email','stripe_payment_intent','product','has_paid')
    readonly_fields = ('stripe_payment_intent',)

    def email(self, obj):
        return obj.customer.email

admin.site.register(OrderDetail,OrderDetails_Admin)