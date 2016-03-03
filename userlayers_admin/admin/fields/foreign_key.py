# coding: utf-8
from userlayers_admin.admin.fields.base import FieldAdmin, FieldFormAdmin


class ForeignKeyFieldFormAdmin(FieldFormAdmin):
    def __init__(self, *args, **kwargs):
        from userlayers_admin.admin import ModelDefinitionAdminBuilder
        super(ForeignKeyFieldFormAdmin, self).__init__(*args, **kwargs)
        self.fields['to'].choices = [(md.pk, md.verbose_name) for md in ModelDefinitionAdminBuilder.get_models()]


class ForeignKeyFieldAdmin(FieldAdmin):
    form = ForeignKeyFieldFormAdmin

    def get_queryset(self, request):
        return super(ForeignKeyFieldAdmin, self).get_queryset(request).prefetch_related('to')

    def get_list_display(self, request):
        return list(super(ForeignKeyFieldAdmin, self).get_list_display(request)) + ['to_human_name']

    # TODO может кеш?
    def to_human_name(self, obj):
        return obj.to

    to_human_name.short_description = 'To'
