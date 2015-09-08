# coding: utf-8
import os
import datetime
import hashlib
from django.conf import settings
from django.db.models import ImageField
from userlayers.models import ModelDef, ModelDefManager


def file_upload_to(instance, filename):
    hd = hashlib.md5(str(datetime.datetime.now())).hexdigest()
    return os.path.join(instance.upload_to, hd[:2], hd[2:4], '%s%s' % (hd, os.path.splitext(filename)[1]))


class MainModelDefManager(ModelDefManager):
    pass


class MainModelDef(ModelDef):
    upload_to = settings.ICON_FOLDER_IN_MEDIA_ROOT

    icon = ImageField(upload_to=file_upload_to, null=True, blank=True, verbose_name=u'иконка')

    objects = MainModelDefManager()

    class Meta:
        app_label = 'main'
        db_table = 'main_modeldefinition'
        ordering = ['id']
        verbose_name = u'модель'
        verbose_name_plural = u'модели'

from main.models.files import *
