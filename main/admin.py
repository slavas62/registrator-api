# coding: utf-8
from django.contrib import admin
from django.db import models as django_models, ProgrammingError
from django import forms as django_forms
from mutant import models as mutant_models
from userlayers.api.forms import FIELD_TYPES
from userlayers.api.naming import translit_and_slugify, get_app_label_for_user, get_db_table_name
from userlayers.models import ModelDefinition


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

    def __init__(self, *args, **kwargs):
        super(ModelDefinitionFormAdmin, self).__init__(*args, **kwargs)
        self.fields['verbose_name'].required = True
        self.fields['verbose_name_plural'].required = True


class ModelDefinitionAdmin(admin.ModelAdmin):
    model = ModelDefinition
    form = ModelDefinitionFormAdmin
    inlines = [FieldDefinitionInlineAdmin]
    exclude = ['managed', 'app_label']
    readonly_fields = ['db_table']
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
                    django_models.AutoField, django_models.ManyToOneRel, django_models.OneToOneField))
                    and f.name not in self.exclude]
            }]]

    def save_model(self, request, obj, form, change):
        slug = translit_and_slugify(obj.name)
        obj.name = slug[:100]
        obj.owner = request.user
        obj.verbose_name = obj.name
        obj.app_label = get_app_label_for_user(request.user)[:100]
        obj.db_table = get_db_table_name(request.user, obj.name)[:63]
        obj.model = slug[:100]
        obj.object_name = slug[:255]
        if obj.pk:
            obj.model_class(force_create=True)
        return super(ModelDefinitionAdmin, self).save_model(request, obj, form, change)

admin.site.register(mutant_models.ModelDefinition, ModelDefinitionAdmin)


class FieldAdmin(admin.ModelAdmin):
    save_as = True


for field_type in dict(FIELD_TYPES).values():
    attrs = {'model': field_type}
    FieldDefAdmin = type('{0}Admin'.format(field_type.__name__), (FieldAdmin,), attrs)
    admin.site.register(field_type, FieldDefAdmin)


def admin_modeldefinition_load():
    try:
        for o in mutant_models.ModelDefinition.objects.all():
            class ModelDefinitionClassAdmin(admin.ModelAdmin):
                pass
            try:
                admin.site.unregister(o.model_class())
            except:
                pass
            admin.site.register(o.model_class(), ModelDefinitionClassAdmin)
    except ProgrammingError as e:
        pass


admin_modeldefinition_load()
