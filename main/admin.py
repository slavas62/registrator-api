# coding: utf-8
from django.contrib import admin
from django.db import models as django_models
from mutant import models as mutant_models


class FieldDefinitionInlineAdmin(admin.TabularInline):
    model = mutant_models.FieldDefinition
    fk_name = 'model_def'
    extra = 0
    suit_classes = 'suit-tab suit-tab-fields'


class ModelDefinitionAdmin(admin.ModelAdmin):
    model = mutant_models.ModelDefinition
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

admin.site.register(mutant_models.ModelDefinition, ModelDefinitionAdmin)