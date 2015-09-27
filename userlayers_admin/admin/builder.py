# coding: utf-8
from copy import deepcopy
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from userlayers import DEFAULT_MD_GEOMETRY_FIELD_TYPE, DEFAULT_MD_GEOMETRY_FIELD_NAME, get_modeldefinition_model
from userlayers.forms import FIELD_TYPES, GEOMETRY_FIELD_TYPES
from django.db.models import ForeignKey
from django.forms import ModelForm, ChoiceField
from userlayers_admin.admin.object.admin_class import get_objects_admin_class

ModelDef = get_modeldefinition_model()


class ModelDefinitionAdminBuilder(object):
    objects_admin_class = get_objects_admin_class()

    class FieldAdmin(admin.ModelAdmin):
        list_display = ['id', 'name', 'verbose_name', 'modeldef']
        exclude = ['editable', 'db_column', 'primary_key', 'content_type']
        save_as = True

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
            return super(ModelDefinitionAdminBuilder.FieldAdmin, self).delete_model(request, obj)

        def save_model(self, request, obj, form, change):
            if change and not self.has_change_permission(request, obj):
                raise PermissionDenied
            return super(ModelDefinitionAdminBuilder.FieldAdmin, self).save_model(request, obj, form, change)

        def modeldef(self, obj):
            return obj.model_def.verbose_name or obj.model_def.name

    def __init__(self):
        def regit(field_type):
            field_content_type = field_type.get_content_type()

            class ThisFieldFormAdmin(ModelForm):
                model = field_type

                def __init__(self, *args, **kwargs):
                    super(ThisFieldFormAdmin, self).__init__(*args, **kwargs)
                    self.fields['model_def'] = ChoiceField(
                        [(md.pk, md.verbose_name) for md in
                         getattr(ModelDef, 'admin_objects_objects', ModelDef.objects).all()])

                def clean(self):
                    cleaned_data = super(ThisFieldFormAdmin, self).clean()
                    if 'model_def' in cleaned_data:
                        cleaned_data['model_def'] = ModelDef.objects.get(pk=cleaned_data['model_def'])
                    return cleaned_data

            class ThisFieldAdmin(self.FieldAdmin):
                form = ThisFieldFormAdmin
                model = field_type

                def get_queryset(self, request):
                    qs = super(ThisFieldAdmin, self) \
                        .get_queryset(request) \
                        .filter(
                        content_type=field_content_type,
                        model_def_id__in=[
                            _['id'] for _ in getattr(ModelDef, 'admin_objects', ModelDef.objects).values('id')]) \
                        .prefetch_related('model_def')
                    return qs

            admin.site.register(field_type, ThisFieldAdmin)

        for field_type in dict(FIELD_TYPES).values():
            regit(field_type)

    def build(self):
        registry = {}
        for m, a in admin.site._registry.items():
            if issubclass(a.__class__, self.objects_admin_class):
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
        return getattr(ModelDef, 'admin_objects_objects', ModelDef.objects).all()

    @classmethod
    def get_admin_class(cls, o):
        class ObjectsFormAdmin(ModelForm):
            foreign_keys = []

            class Meta:
                model = o.model_class()

            def __init__(self, *args, **kwargs):
                super(ObjectsFormAdmin, self).__init__(*args, **kwargs)
                model_fields = dict((f.name, f) for f in self.instance._meta.fields)
                md_fields = dict((f.name, f) for f in o.fielddefinitions.select_subclasses())
                fields = {}
                for name, field in self.fields.items():
                    model_field = model_fields.get(name)
                    md_field = md_fields.get(name)
                    if isinstance(model_field, ForeignKey):
                        self.foreign_keys.append(name)
                        field.queryset = ContentType.objects.get_for_id(md_field.to.pk).model_class().objects.all()
                    fields[name] = field
                self.fields = fields

            def clean(self):
                su = super(ObjectsFormAdmin, self).clean()
                # TODO это просто бомба же
                for name in self.foreign_keys:
                    su[name] = ContentType(id=su[name].pk)
                return su

        class ObjectsAdmin(cls.objects_admin_class):
            form = ObjectsFormAdmin
            fieldsets = [[
                None,
                {
                    'classes': ['suit-tab', 'suit-tab-general'],
                    'fields': [f.name for f in o.fielddefinitions.select_subclasses().order_by('pk')
                               if f.editable and not hasattr(f, 'auto_now_add') or not f.auto_now_add]
                }
            ]]

        return ObjectsAdmin
