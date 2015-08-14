# coding: utf-8
from django.contrib import admin
from django.db import models as django_models
from django import forms as django_forms
from mutant import models as mutant_models


class FieldDefinitionInlineAdmin(admin.TabularInline):
    model = mutant_models.FieldDefinition
    fk_name = 'model_def'
    extra = 0
    suit_classes = 'suit-tab suit-tab-fields'

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]


class ModelDefinitionFormAdmin(django_forms.ModelForm):
    class Meta:
        model = mutant_models.ModelDefinition

    def __init__(self, *args, **kwargs):
        if 'initial' not in kwargs:
            kwargs['initial'] = {}
        kwargs['initial'].update({'app_label': 'ul_1'})
        super(ModelDefinitionFormAdmin, self).__init__(*args, **kwargs)
        self.fields['app_label'].widget.attrs['readonly'] = True


class ModelDefinitionAdmin(admin.ModelAdmin):
    model = mutant_models.ModelDefinition
    form = ModelDefinitionFormAdmin
    inlines = [FieldDefinitionInlineAdmin]
    suit_form_tabs = [
        ['general', u'Тип'],
        ['fields', u'Поля'],
    ]

    def __init__(self, model, admin_site):
        super(ModelDefinitionAdmin, self).__init__(model, admin_site)
        self.fieldsets = [[
            None,
            {
                'classes': ('suit-tab', 'suit-tab-general',),
                'fields': [f.name for f in self.opts.fields if not isinstance(f, (
                    django_models.AutoField, django_models.ManyToOneRel, django_models.OneToOneField))]
            }]]

    def save_model(self, request, obj, form, change):
        super(ModelDefinitionAdmin, self).save_model(request, obj, form, change)
        obj.model_class(force_create=True)


admin.site.register(mutant_models.ModelDefinition, ModelDefinitionAdmin)


for o in mutant_models.ModelDefinition.objects.all():
    class ModelDefinitionClassAdmin(admin.ModelAdmin):
        pass
    admin.site.register(o.model_class(), ModelDefinitionClassAdmin)


for field_type in mutant_models.FieldDefinitionBase._field_definitions.values():
    attrs = {'model': field_type}
    FieldDefAdmin = type('{0}Admin'.format(field_type.__name__), (admin.ModelAdmin,), attrs)
    admin.site.register(field_type, FieldDefAdmin)
