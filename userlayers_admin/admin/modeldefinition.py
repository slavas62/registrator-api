# coding: utf-8
from ordered_set import OrderedSet
from django import forms
from django.contrib import admin
from django.core.exceptions import NON_FIELD_ERRORS
from mutant.models import FieldDefinition
from userlayers import DEFAULT_MD_GEOMETRY_FIELD_TYPE, DEFAULT_MD_GEOMETRY_FIELD_NAME, \
    USERLAYERS_MD_CLASS_RESERVED_NAMES, get_modeldefinition_model
from userlayers.forms import FIELD_TYPES, GEOMETRY_FIELD_TYPES
from userlayers.models import ModelDefFieldOrder
from suit.admin import SortableTabularInline

ModelDef = get_modeldefinition_model()


class FieldDefinitionInlineAdmin(admin.TabularInline):
    model = FieldDefinition
    fk_name = 'model_def'
    suit_classes = 'suit-tab suit-tab-fields'
    fields = ['id', 'content_type', 'name', 'verbose_name', 'null', 'blank']

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields if f.name != 'order']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


class ModelDefinitionFormAdmin(forms.ModelForm):
    GEOMETRY_FIELD_CHOICES = [(n, c._meta.verbose_name) for n, c in dict(GEOMETRY_FIELD_TYPES).items()]
    GEOMETRY_FIELD_LABEL = u'Геометрия по умолчанию'
    geometry_field = forms.ChoiceField(choices=GEOMETRY_FIELD_CHOICES, label=GEOMETRY_FIELD_LABEL)

    class Meta:
        model = ModelDef
        widgets = {
            'verbose_name': forms.TextInput(),
            'verbose_name_plural': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ModelDefinitionFormAdmin, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance:
            geomentry_field = instance.fielddefinitions.select_subclasses().filter(
                name=DEFAULT_MD_GEOMETRY_FIELD_NAME).first()
            if geomentry_field:
                self.fields['geometry_field'] = forms.CharField(initial=geomentry_field._meta.verbose_name,
                                                                label=self.GEOMETRY_FIELD_LABEL)
                self.fields['geometry_field'].widget.attrs["readonly"] = True

    def is_valid(self):
        is_valid = super(ModelDefinitionFormAdmin, self).is_valid()
        if self.cleaned_data['name'] in USERLAYERS_MD_CLASS_RESERVED_NAMES:
            self._errors[NON_FIELD_ERRORS] = '"%s" is reserved name' % self.cleaned_data['name']
            return super(ModelDefinitionFormAdmin, self).is_valid()
        return is_valid


def get_inline(field_type):
    field_content_type = field_type.get_content_type()

    class Form(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super(Form, self).__init__(*args, **kwargs)
            self.initial.update({'content_type': field_content_type})

        class Meta:
            model = field_type
            widgets = {
                'verbose_name': forms.TextInput(),
                'verbose_name_plural': forms.TextInput(),
                'content_type': forms.TextInput(),
            }

    class Inline(admin.TabularInline):
        model = field_type
        fk_name = 'model_def'
        exclude = ['db_column', 'db_index', 'help_text', 'editable', 'primary_key', 'unique', 'unique_for_date',
                   'unique_for_month', 'unique_for_year']
        form = Form
        suit_classes = 'suit-tab suit-tab-fields'
        extra = 0

        def get_queryset(self, request):
            return super(Inline, self).get_queryset(request).filter(content_type=field_content_type)

    return Inline


class ModelDefinitionAdmin(admin.ModelAdmin):
    form = ModelDefinitionFormAdmin
    inlines = [FieldDefinitionInlineAdmin]
    # inlines = []
    # for field_type in dict(FIELD_TYPES).values():
    #     inlines.append(get_inline(field_type))

    list_display = ['verbose_name', 'name', 'model']
    fieldsets = [[
        None,
        {
            'classes': ['suit-tab', 'suit-tab-general'],
            'fields': OrderedSet(['name', 'owner', 'geometry_field', 'verbose_name', 'verbose_name_plural'] +
                                 [_.name for _ in ModelDef._meta.local_concrete_fields if
                                  _.name not in getattr(ModelDef, 'admin_exclude_fields', []) + ['modeldef_ptr']])
        }
    ]]
    suit_form_tabs = [
        ['general', u'Тип'],
        ['fields', u'Поля'],
    ]

    def get_queryset(self, request):
        return getattr(ModelDef, 'admin_objects', ModelDef.objects).all()

    def save_model(self, request, obj, form, change):
        super(ModelDefinitionAdmin, self).save_model(request, obj, form, change)
        if not change:
            geometry_model = dict(GEOMETRY_FIELD_TYPES).get(
                form.cleaned_data.get('geometry_field', DEFAULT_MD_GEOMETRY_FIELD_TYPE))
            geometry_field = geometry_model(
                name=DEFAULT_MD_GEOMETRY_FIELD_NAME, model_def=obj, null=True, blank=True)
            geometry_field.save()
