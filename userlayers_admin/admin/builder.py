# coding: utf-8
from copy import deepcopy
from django.contrib import admin
from django.core.exceptions import PermissionDenied
from userlayers import DEFAULT_MD_GEOMETRY_FIELD_TYPE, DEFAULT_MD_GEOMETRY_FIELD_NAME, get_modeldefinition_model
from userlayers.api.forms import FIELD_TYPES, GEOMETRY_FIELD_TYPES
from userlayers_admin.admin.object.admin_class import get_objects_admin_class

ModelDef = get_modeldefinition_model()


class ModelDefinitionAdminBuilder(object):
    objects_admin_class = get_objects_admin_class()

    class FieldAdmin(admin.ModelAdmin):
        exclude = ['editable', 'db_column', 'primary_key']
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

    def __init__(self):
        for field_type in dict(FIELD_TYPES).values():
            attrs = {'model': field_type}
            o = type('{0}Admin'.format(field_type.__name__), (self.FieldAdmin,), attrs)
            admin.site.register(field_type, o)

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
        class ObjectsAdmin(cls.objects_admin_class):
            fieldsets = [[
                None,
                {
                    'classes': ['suit-tab', 'suit-tab-general'],
                    'fields': [f.name for f in o.fielddefinitions.select_subclasses().order_by('pk')
                               if f.editable and not hasattr(f, 'auto_now_add') or not f.auto_now_add]
                }
            ]]

        return ObjectsAdmin
