# coding: utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from tastypie.models import ApiKey


class MainUserApiKeyInlineAdmin(admin.TabularInline):
    model = ApiKey
    can_delete = False
    fields = readonly_fields = ['key']


UserAdmin.inlines = [MainUserApiKeyInlineAdmin]
