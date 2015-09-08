# coding: utf-8
from django.db import models
from django.conf import settings
from sorl.thumbnail import ImageField
from main.models import file_upload_to


class ResourceVideo(models.Model):
    upload_to = settings.RESOURCE_FOLDER_VIDEO_IN_MEDIA_ROOT

    file = models.FileField(upload_to=file_upload_to, null=False, blank=False, verbose_name=u'файл')
    object = models.ForeignKey('main.MainModelDef', null=True, blank=True, related_name=u'videos', verbose_name=u'объект')

    class Meta:
        app_label = 'main'
        db_table = 'main_resource_video'
        verbose_name = u'video'
        verbose_name_plural = u'videos'


class ResourceImage(models.Model):
    upload_to = settings.RESOURCE_FOLDER_IMAGE_IN_MEDIA_ROOT

    file = ImageField(upload_to=file_upload_to, null=False, blank=False, verbose_name=u'файл')
    object = models.ForeignKey('main.MainModelDef', null=True, blank=True, related_name=u'images', verbose_name=u'объект')

    class Meta:
        app_label = 'main'
        db_table = 'main_resource_image'
        verbose_name = u'image'
        verbose_name_plural = u'images'
