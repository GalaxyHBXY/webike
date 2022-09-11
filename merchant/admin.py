from django.contrib import admin

# Register your models here.
from merchant.models import Merchant


class Merchant_Admin(admin.ModelAdmin):
    list_display = ('id', 'merchant_name', 'email', 'abn', 'abn_verified')
    search_fields = ('user__email', 'merchant_name')
    readonly_fields = ('id', 'date_joined', 'last_login')
    ordering = ('-user__id',)

    # for display boolean as an icon
    # @admin.display(boolean=True)

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


admin.site.register(Merchant, Merchant_Admin)
