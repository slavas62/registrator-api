# coding: utf-8
from django.forms import ModelForm, FileField
from django.contrib.admin import TabularInline
from userlayers_admin.admin.object import ModelDefinitionObjectAdmin


class MainModelDefinitionObjectAdmin(ModelDefinitionObjectAdmin):
    suit_form_tabs = ModelDefinitionObjectAdmin.suit_form_tabs + [
        ['images', u'Изображения'],
        ['videos', u'Видео'],
    ]

    def get_inline_instances(self, request, obj=None):
        self.inlines = []

        class InlineForm(ModelForm):
            def __init__(self, *args, **kwargs):
                super(InlineForm, self).__init__(*args, **kwargs)
                self.fields['file'] = FileField()

        for f in self.model._meta.get_all_related_objects(local_only=True):
            attrs = {
                'model': f.model,
                'extra': 0,
                'suit_classes': 'suit-tab suit-tab-%s' % f.field.rel.related_name,
                'form': InlineForm
            }
            o = type('{0}InlineAdmin'.format(f.field.rel.related_name), (TabularInline,), attrs)
            self.inlines.append(o)

        return super(MainModelDefinitionObjectAdmin, self).get_inline_instances(request, obj)
