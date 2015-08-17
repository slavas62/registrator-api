# coding: utf-8
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as UserAdminBase, GroupAdmin as BaseGroupAdmin
from django.utils.translation import ugettext_lazy as _
from django import forms
from acc.models import User


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


class GroupForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        label=u'Пользователи',
        queryset=User.objects.all(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple("users", is_stacked=False)
    )

    class Meta:
        model = Group
        widgets = {
            'permissions': admin.widgets.FilteredSelectMultiple("permissions", is_stacked=False),
        }


class GroupAdmin(BaseGroupAdmin):
    form = GroupForm

    def save_model(self, request, obj, form, change):
        super(GroupAdmin, self).save_model(request, obj, form, change)
        obj.user_set.clear()
        for user in form.cleaned_data['users']:
             obj.user_set.add(user)

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.form.base_fields['users'].initial = [o.pk for o in obj.user_set.all()]
        else:
            self.form.base_fields['users'].initial = []
        return GroupForm

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
