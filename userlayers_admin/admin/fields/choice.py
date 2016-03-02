# coding: utf-8
from userlayers_admin.admin.fields.base import FieldAdmin, FieldFormAdmin
from djjsoneditor.widgets import JSONEditorWidget


class ChoiceFieldFormAdmin(FieldFormAdmin):
    class Meta(FieldFormAdmin.Meta):
        widgets = {
            'the_choices': JSONEditorWidget()
        }

    def __init__(self, *args, **kwargs):
        super(ChoiceFieldFormAdmin, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ChoiceFieldFormAdmin, self).clean()
        return cleaned_data


class ChoiceFieldAdmin(FieldAdmin):
    form = ChoiceFieldFormAdmin

    def save_model(self, request, obj, form, change):
        obj.the_choices = form.cleaned_data['the_choices']
        return super(ChoiceFieldAdmin, self).save_model(request, obj, form, change)
