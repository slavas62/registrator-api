# coding: utf-8
import os
from django import forms
from django.conf import settings
from django.core.files.base import File
from django.db import models

from django.contrib.admin import TabularInline
from sorl.thumbnail.admin.current import AdminImageWidget
from userlayers import get_modeldefinition_model
from userlayers_admin.admin.modeldefinition import ModelDefinitionAdmin, ModelDefinitionFormAdmin
from userlayers_admin.admin.object import ModelDefinitionObjectAdmin
from main.contrib.helper import generate_filename

ModelDef = get_modeldefinition_model()


class MainModelDefinitionFormAdmin(ModelDefinitionFormAdmin):
    class Meta:
        model = ModelDef
        widgets = {
            'verbose_name': forms.TextInput(),
            'verbose_name_plural': forms.TextInput(),
            'icon': AdminImageWidget(),
        }


class MainModelDefinitionAdmin(ModelDefinitionAdmin):
    form = MainModelDefinitionFormAdmin


class MainModelDefinitionObjectAdmin(ModelDefinitionObjectAdmin):
    suit_form_tabs = ModelDefinitionObjectAdmin.suit_form_tabs + [
        ['images', u'Изображения'],
        ['videos', u'Видео'],
    ]

    def get_inline_instances(self, request, obj=None):
        self.inlines = []

        class InlineForm(forms.ModelForm):
            upload_to = os.path.join(settings.MEDIA_ROOT)
            file_field_class = forms.FileField
            name = None

            def __init__(self, *args, **kwargs):
                instance = kwargs.get('instance', None)
                if instance:
                    file_path = instance.file
                    instance.file = models.ImageField()
                    instance.file.url = ('%s%s' % (settings.MEDIA_URL, file_path)).replace('//', '/')
                    instance.file.file = File(file_path)
                    instance.file.__unicode__ = lambda: file_path
                kwargs['instance'] = instance
                super(InlineForm, self).__init__(*args, **kwargs)
                self.fields['file'] = self.file_field_class(required=True, label=u'файл')

            def save(self, *args, **kwargs):
                self.instance.file = self.handle_uploaded_file(self.cleaned_data['file'])
                return super(InlineForm, self).save(*args, **kwargs)

            def handle_uploaded_file(self, f):
                dst = os.path.join(self.upload_to, generate_filename(str(f)))
                dst_dir = os.path.dirname(dst)
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                with open(dst, 'wb+') as dst_file:
                    for chunk in f.chunks():
                        dst_file.write(chunk)
                    dst_file.close()
                return dst.replace(settings.MEDIA_ROOT, '')

        for f in self.model._meta.get_all_related_objects(local_only=True):
            attrs = {
                'name': f.field.rel.related_name,
                'upload_to': os.path.join(InlineForm.upload_to, getattr(
                    settings, 'RESOURCE_FOLDER_%s_IN_MEDIA_ROOT' % f.field.rel.related_name.upper()))
            }
            if 'image' in f.field.rel.related_name:
                attrs['file_field_class'] = forms.ImageField
            formclass = type('{0}InlineForm'.format(f.field.rel.related_name), (InlineForm,), attrs)
            attrs = {
                'model': f.model,
                'extra': 0,
                'suit_classes': 'suit-tab suit-tab-%s' % f.field.rel.related_name,
                'form': formclass
            }
            adminclass = type('{0}InlineAdmin'.format(f.field.rel.related_name), (TabularInline,), attrs)
            self.inlines.append(adminclass)
        return super(MainModelDefinitionObjectAdmin, self).get_inline_instances(request, obj)
