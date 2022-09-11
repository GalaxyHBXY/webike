from django.contrib import admin

# Register your models here.
from customer.models import Customer


class Customer_Admin(admin.ModelAdmin):
    list_display = ('id', 'email')
    search_fields = ('user__email',)
    readonly_fields = ('id', 'date_joined', 'last_login')
    ordering = ('-user__id',)

    def email(self, obj):
        return obj.user.email

    def is_staff(self, obj):
        return obj.user.is_staff

    def id(self, obj):
        return obj.user.id

    def date_joined(self, obj):
        return obj.user.date_joined

    def last_login(self, obj):
        return obj.user.last_login


admin.site.register(Customer, Customer_Admin)
