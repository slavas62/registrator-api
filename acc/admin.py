# coding: utf-8
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.utils.translation import ugettext_lazy as _
from acc.models import User


admin.site.unregister(Group)


# @admin.register(User)
class UserAdmin(UserAdminBase):
    list_display = ['username', 'is_superuser', 'is_staff']
    list_filter = ['is_superuser']
    search_fields = ['email']
    suit_form_tabs = [['general', u'Основные с-ва']]
    fieldsets = (
        (None, {
            'fields': ['username', 'password'],
            'classes': ['suit-tab', 'suit-tab-general']
        }),
        (_('Personal info'), {
            'fields': ['first_name', 'last_name'],
            'classes': ['suit-tab', 'suit-tab-general']
        }),
        (_('Permissions'), {
            'fields': ['is_active', 'is_staff', 'is_superuser'],
            'classes': ['suit-tab', 'suit-tab-general']
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)
