# coding: utf-8
from copy import deepcopy
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from userlayers import get_modeldefinition_model
from userlayers.forms import FIELD_TYPES
from django.db.models import ForeignKey
from django.forms import ModelForm
from userlayers_admin.admin.object.admin_class import get_objects_admin_class
from userlayers_admin.admin.fields import FIELD_TYPES_ADMIN_CLASS

ModelDef = get_modeldefinition_model()


class ModelDefinitionAdminBuilder(object):
    objects_admin_class = get_objects_admin_class()

    def build(self):
        # fields
        for field_type_name, field_type_admin_class in FIELD_TYPES_ADMIN_CLASS.items():
            try:
                field_type = dict(FIELD_TYPES).get(field_type_name, None)
                admin.site.register(field_type, field_type_admin_class)
            except:
                pass

        # models
        registry = {}
        for m, a in admin.site._registry.items():
            if issubclass(a.__class__, self.objects_admin_class):
                continue
            registry[m] = a
        admin.site._registry = registry
        errs = []
        for o in self.get_models():
            try:
                self._build_one(o)
            except:
                errs.append(o)
        for o in errs:
            self._build_one(o)

    def _build_one(self, o):
        c = o.model_class()
        cc = deepcopy(c)
        cc._meta.app_label = 'objects'
        admin.site.register(cc, self.get_admin_class(o))

    @classmethod
    def get_models(cls):
        return getattr(ModelDef, 'admin_objects_objects', ModelDef.objects).all()

    @classmethod
    def get_admin_class(cls, o):
        class ObjectsFormAdmin(ModelForm):
            foreign_keys = []
            foreign_keys_models_with_magic = [User]

            class Meta:
                model = o.model_class()

            def __init__(self, *args, **kwargs):
                super(ObjectsFormAdmin, self).__init__(*args, **kwargs)
                self.model_fields = dict((f.name, f) for f in self.instance._meta.fields)
                self.md_fields = dict((f.name, f) for f in o.fielddefinitions.select_subclasses())
                fields = {}
                for name, field in self.fields.items():
                    model_field = self.model_fields.get(name)
                    md_field = self.md_fields.get(name)
                    if isinstance(model_field, ForeignKey):
                        self.foreign_keys.append(name)
                        field.queryset = ContentType.objects.get_for_id(md_field.to.pk).model_class().objects.all()
                    fields[name] = field
                self.fields = fields

            def clean(self):
                su = super(ObjectsFormAdmin, self).clean()
                # TODO это просто бомба же
                for name in self.foreign_keys:
                    if self.md_fields.get(name).to.model_class() in self.foreign_keys_models_with_magic:
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
