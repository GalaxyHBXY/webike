from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from user.models import User


class User_Admin(UserAdmin):
    list_display = ('id', 'email', 'user_type')
    fieldsets = (
        (None, {'fields': ('password', 'user_type', 'status')}),
        (_('Personal info'), {'fields': ('email', 'phone')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    search_fields = ('email',)
    ordering = ('id',)

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


admin.site.register(User, User_Admin)
admin.site.unregister(Group)
