# coding: utf-8
from django.forms import ChoiceField
from userlayers_admin.admin.fields.base import FieldAdmin, FieldFormAdmin, ModelDef


class ForeignKeyFieldFormAdmin(FieldFormAdmin):
    def __init__(self, *args, **kwargs):
        super(ForeignKeyFieldFormAdmin, self).__init__(*args, **kwargs)
        self.fields['to'] = ChoiceField(
            [(md.pk, md.verbose_name) for md in
             getattr(ModelDef, 'admin_objects_objects', ModelDef.objects).all()])

    def clean(self):
        cleaned_data = super(ForeignKeyFieldFormAdmin, self).clean()
        if 'to' in cleaned_data:
            cleaned_data['to'] = ModelDef.objects.get(pk=cleaned_data['to'])
        return cleaned_data


class ForeignKeyFieldAdmin(FieldAdmin):
    form = ForeignKeyFieldFormAdmin

    def get_list_display(self, request):
        return list(super(ForeignKeyFieldAdmin, self).get_list_display(request)) + ['to_human_name']

    # TODO может кеш?
    def to_human_name(self, obj):
        return ModelDef.objects.get(name=obj.to).verbose_name

    to_human_name.short_description = 'To'
