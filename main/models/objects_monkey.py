# coding: utf-8
from django.conf import settings
from django.db.models.fields import FilePathField
from userlayers import get_modeldefinition_model
from registrator.contrib.fix_exif import fix_exif

try:
    for md in get_modeldefinition_model().objects.all():
        model = md.model_class()


        def save(self, *args, **kwargs):
            super(self.__class__, self).save(*args, **kwargs)
            for field in self.__class__._meta.fields:
                if isinstance(field, FilePathField):
                    filepath = ('%s/%s' % (settings.MEDIA_ROOT, getattr(self, field.name))).replace('//', '/')
                    fix_exif(filepath)


        model.save = save
except:
    pass
