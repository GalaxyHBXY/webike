from django.contrib import admin
from .models import *


class OrderDetails_Admin(admin.ModelAdmin):
    list_display=('email','session_id','product','has_paid','created_on')
    readonly_fields = ('session_id',)

    def email(self, obj):
        return obj.customer.email

admin.site.register(OrderDetail,OrderDetails_Admin)