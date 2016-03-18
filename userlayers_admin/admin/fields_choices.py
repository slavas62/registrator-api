# coding: utf-8
from django.contrib import admin
from django import forms
from mutant.models import FieldDefinition, FieldDefinitionChoice

from userlayers import get_modeldefinition_model
from userlayers_admin.admin import ModelDefinitionAdminBuilder

ModelDef = get_modeldefinition_model()

__all__ = []


class FieldDefinitionChoiceAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FieldDefinitionChoiceAdminForm, self).__init__(*args, **kwargs)
        mds = [_['id'] for _ in ModelDefinitionAdminBuilder.get_models().values('id')]
        md_fields = FieldDefinition.objects.order_by('model_def', 'id').prefetch_related('model_def')
        self.fields['field_def'].choices = [
            (f.id, '%s . %s (%s)' % (f.model_def.verbose_name, f.verbose_name, f.name))
            for f in md_fields
            if f.model_def.id in mds]


class FieldDefinitionChoiceAdmin(admin.ModelAdmin):
    form = FieldDefinitionChoiceAdminForm
    save_as = True
    list_display = ['md_name', 'field_name', 'group', 'label', 'value']

    def get_queryset(self, request):
        return super(FieldDefinitionChoiceAdmin, self).get_queryset(request).prefetch_related(
            'field_def', 'field_def__model_def').order_by(
            'field_def__model_def', 'field_def__verbose_name', 'group', 'value')

    def md_name(self, obj):
        return obj.field_def.model_def.verbose_name
    md_name.short_description = u'Модель'

    def field_name(self, obj):
        return '%s (%s)' % (obj.field_def.verbose_name, obj.field_def.name)
    field_name.short_description = u'Поле'

admin.site.register(FieldDefinitionChoice, FieldDefinitionChoiceAdmin)
