# coding: utf-8
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.db import models as django_models, ProgrammingError
from django import forms as django_forms
from mutant import models as mutant_models
from userlayers.api.forms import FIELD_TYPES
from userlayers.models import ModelDefinition
from suit.config import settings


class FieldDefinitionInlineAdmin(admin.TabularInline):
    model = mutant_models.FieldDefinition
    fk_name = 'model_def'
    suit_classes = 'suit-tab suit-tab-fields'

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


class ModelDefinitionFormAdmin(django_forms.ModelForm):
    class Meta:
        model = ModelDefinition
        widgets = {
            'verbose_name': django_forms.TextInput(),
            'verbose_name_plural': django_forms.TextInput(),
        }


class ModelDefinitionAdmin(admin.ModelAdmin):
    model = ModelDefinition
    form = ModelDefinitionFormAdmin
    inlines = [FieldDefinitionInlineAdmin]
    fieldsets = [[
        None,
        {
            'classes': ['suit-tab', 'suit-tab-general'],
            'fields': ['owner', 'name', 'verbose_name', 'verbose_name_plural']
        }
    ]]
    suit_form_tabs = [
        ['general', u'Тип'],
        ['fields', u'Поля'],
    ]

admin.site.register(ModelDefinition, ModelDefinitionAdmin)


class FieldAdmin(admin.ModelAdmin):
    save_as = True


for field_type in dict(FIELD_TYPES).values():
    attrs = {'model': field_type}
    FieldDefAdmin = type('{0}Admin'.format(field_type.__name__), (FieldAdmin,), attrs)
    admin.site.register(field_type, FieldDefAdmin)


def admin_modeldefinition_unload():
    menu = []
    for o in ModelDefinition.objects.all():
        # for m in settings.SUIT_CONFIG['MENU'][settings.SUIT_CONFIG['MENU_USERLAYERS_MODELS']]['models']:
        #     if m['model'] != unicode(o):
        #         menu.append(m)
        try:
            admin.site.unregister(o.model_class())
        except:
            pass


def admin_modeldefinition_load():
    class ModelDefinitionClassAdmin(admin.ModelAdmin):
        pass
    for o in ModelDefinition.objects.all():
        try:
            admin.site.register(o.model_class(), ModelDefinitionClassAdmin)
            # settings.SUIT_CONFIG['MENU'][settings.SUIT_CONFIG['MENU_USERLAYERS_MODELS']]['models'].append(
            #     {'label': '%s %s' % (o.app_label.upper(), o.verbose_name.capitalize()), 'model': unicode(o)})
        except AlreadyRegistered as e:
            pass

admin_modeldefinition_load()
