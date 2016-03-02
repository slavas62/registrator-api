# coding: utf-8
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from mutant.contrib.related.models import ForeignKeyDefinition
from userlayers import DEFAULT_MD_GEOMETRY_FIELD_NAME, get_modeldefinition_model
from django.forms import ModelForm, ChoiceField

__all__ = ['FieldAdmin', 'FieldFormAdmin']

ModelDef = get_modeldefinition_model()


class FieldFormAdmin(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FieldFormAdmin, self).__init__(*args, **kwargs)
        self.fields['model_def'] = ChoiceField(
            [(md.pk, md.verbose_name) for md in
             getattr(ModelDef, 'admin_objects_objects', ModelDef.objects).all()])
        # sorry
        if 'ForeignKeyDefinition' in str(self._meta.model):
            self.fields['to'] = ChoiceField(
                [(md.pk, md.verbose_name) for md in
                 getattr(ModelDef, 'admin_objects_objects', ModelDef.objects).all()])

    def clean(self):
        cleaned_data = super(FieldFormAdmin, self).clean()
        if 'model_def' in cleaned_data:
            cleaned_data['model_def'] = ModelDef.objects.get(pk=cleaned_data['model_def'])
        if 'ForeignKeyDefinition' in str(self._meta.model) and 'to' in cleaned_data:
            cleaned_data['to'] = ModelDef.objects.get(pk=cleaned_data['to'])
        return cleaned_data


class FieldAdmin(admin.ModelAdmin):
    form = FieldFormAdmin

    list_display = ['id', 'name', 'verbose_name', 'modeldef']
    exclude = ['editable', 'db_column', 'primary_key', 'content_type']
    save_as = True

    def get_queryset(self, request):
        qs = super(FieldAdmin, self) \
            .get_queryset(request) \
            .filter(
            content_type=self.model.get_content_type(),
            model_def_id__in=[
                _['id'] for _ in getattr(ModelDef, 'admin_objects', ModelDef.objects).values('id')]) \
            .prefetch_related('model_def')
        return qs

    def get_actions(self, request):
        return {}

    def has_change_permission(self, request, obj=None):
        if obj and obj.name == DEFAULT_MD_GEOMETRY_FIELD_NAME:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

    def delete_model(self, request, obj):
        if not self.has_delete_permission(request, obj):
            raise PermissionDenied
        if isinstance(obj, ForeignKeyDefinition):
            super(FieldAdmin, self).delete_model(request, obj)
        return super(FieldAdmin, self).delete_model(request, obj)

    def save_model(self, request, obj, form, change):
        if change and not self.has_change_permission(request, obj):
            raise PermissionDenied
        return super(FieldAdmin, self).save_model(request, obj, form, change)

    def modeldef(self, obj):
        return obj.model_def.verbose_name or obj.model_def.name
