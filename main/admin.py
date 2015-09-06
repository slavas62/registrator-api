# coding: utf-8
from copy import deepcopy
import mutant
from django.contrib import admin
from django import forms as django_forms
from userlayers.api.forms import FIELD_TYPES, GEOMETRY_FIELD_TYPES
from userlayers.models import ModelDefinition


class FieldDefinitionInlineAdmin(admin.TabularInline):
    model = mutant.models.FieldDefinition
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
    # geometry_field = django_forms.CharField(
    #     widget=django_forms.Select(
    #         choices=[(_, _) for _ in dict(GEOMETRY_FIELD_TYPES).keys()]), label=u'Геометрия по умолчанию')

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
            'fields': ['name', 'owner',
                       # 'geometry_field',
                       'verbose_name', 'verbose_name_plural']
        }
    ]]
    suit_form_tabs = [
        ['general', u'Тип'],
        ['fields', u'Поля'],
    ]

admin.site.register(ModelDefinition, ModelDefinitionAdmin)


class ModelDefinitionAdminBuilder(object):
    class AdminClass(admin.ModelAdmin):
        form = ModelDefinitionFormAdmin

    class FieldAdmin(admin.ModelAdmin):
        exclude = ['editable', 'db_column', 'primary_key']
        save_as = True

    def __init__(self):
        for field_type in dict(FIELD_TYPES).values():
            attrs = {'model': field_type}
            o = type('{0}Admin'.format(field_type.__name__), (self.FieldAdmin,), attrs)
            admin.site.register(field_type, o)

    def build(self):
        registry = {}
        for m, a in admin.site._registry.items():
            if issubclass(a.__class__, self.AdminClass):
                continue
            registry[m] = a
        admin.site._registry = registry
        for o in self.get_models():
            c = o.model_class()
            cc = deepcopy(c)
            cc._meta.app_label = 'objects'
            admin.site.register(cc, self.get_admin_class(o))

    @classmethod
    def get_models(cls):
        return ModelDefinition.objects.all()

    @classmethod
    def get_admin_class(cls, o):
        class Alass(cls.AdminClass):
            fields = [f.name for f in o.fielddefinitions.order_by('pk')]
        return Alass

builder = ModelDefinitionAdminBuilder()
builder.build()
