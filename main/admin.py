# coding: utf-8
from copy import deepcopy
from django import forms
from django.contrib import admin
from django.db import ProgrammingError
from mutant.models import FieldDefinition
from userlayers import DEFAULT_MD_GEOMETRY_FIELD_TYPE, DEFAULT_MD_GEOMETRY_FIELD_NAME
from userlayers.models import ModelDefinition
from userlayers.api.forms import FIELD_TYPES, GEOMETRY_FIELD_TYPES


class FieldDefinitionInlineAdmin(admin.TabularInline):
    model = FieldDefinition
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


class ModelDefinitionFormAdmin(forms.ModelForm):
    GEOMETRY_FIELD_CHOICES = [(n, c._meta.verbose_name) for n, c in dict(GEOMETRY_FIELD_TYPES).items()]
    GEOMETRY_FIELD_LABEL = u'Геометрия по умолчанию'
    geometry_field = forms.ChoiceField(choices=GEOMETRY_FIELD_CHOICES, label=GEOMETRY_FIELD_LABEL)

    class Meta:
        model = ModelDefinition
        widgets = {
            'verbose_name': forms.TextInput(),
            'verbose_name_plural': forms.TextInput(),
        }

    def __init__(self, instance=None, *args, **kwargs):
        super(ModelDefinitionFormAdmin, self).__init__(instance=instance, *args, **kwargs)
        if instance:
            geomentry_field = FieldDefinition.objects.get_by_natural_key(
                instance.app_label, instance.object_name, DEFAULT_MD_GEOMETRY_FIELD_NAME)
            gt = dict(GEOMETRY_FIELD_TYPES)
            self.fields['geometry_field'] = forms.ChoiceField(
                initial=gt.keys()[gt.values().index(geomentry_field.__class__)],
                choices=self.GEOMETRY_FIELD_CHOICES, label=self.GEOMETRY_FIELD_LABEL)
            self.fields['geometry_field'].widget.attrs["disabled"] = True


class ModelDefinitionAdmin(admin.ModelAdmin):
    model = ModelDefinition
    form = ModelDefinitionFormAdmin

    inlines = [FieldDefinitionInlineAdmin]
    fieldsets = [[
        None,
        {
            'classes': ['suit-tab', 'suit-tab-general'],
            'fields': ['name', 'owner', 'geometry_field', 'verbose_name', 'verbose_name_plural']
        }
    ]]
    suit_form_tabs = [
        ['general', u'Тип'],
        ['fields', u'Поля'],
    ]

    def save_model(self, request, obj, form, change):
        super(ModelDefinitionAdmin, self).save_model(request, obj, form, change)
        if not change:
            geometry_model = dict(GEOMETRY_FIELD_TYPES).get(
                form.cleaned_data.get('geometry_field', DEFAULT_MD_GEOMETRY_FIELD_TYPE))
            geometry_field = geometry_model(
                name=DEFAULT_MD_GEOMETRY_FIELD_NAME, model_def=obj, null=True, blank=True)
            geometry_field.save()


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
            try:
                c = o.model_class()
                cc = deepcopy(c)
                cc._meta.app_label = 'objects'
                admin.site.register(cc, self.get_admin_class(o))
            except:
                pass

    @classmethod
    def get_models(cls):
        return ModelDefinition.objects.all()

    @classmethod
    def get_admin_class(cls, o):
        class Alass(cls.AdminClass):
            fields = [f.name for f in o.fielddefinitions.order_by('pk')]

        return Alass


builder = ModelDefinitionAdminBuilder()
# catch syncdb exception
try:
    builder.build()
except ProgrammingError as e:
    pass
