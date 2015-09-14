# coding: utf-8
from django.conf import settings
from django.db.models import ImageField, BooleanField, PositiveSmallIntegerField
from userlayers.models import ModelDef, ModelDefManager
from main.contrib.helper import upload_to_generate_filename


class MainModelDefManager(ModelDefManager):
    pass


class MainModelDefAdminManager(MainModelDefManager):
    def get_queryset(self):
        return super(MainModelDefAdminManager, self).get_queryset().filter(hidden=False)


class MainModelDefObjectsAdminManager(MainModelDefAdminManager):
    pass


class MainModelDef(ModelDef):
    upload_to = settings.ICON_FOLDER_IN_MEDIA_ROOT

    RESOURCE_TYPE_CHOICES_IMAGE = 1
    RESOURCE_TYPE_CHOICES_VIDEO = 2
    RESOURCE_TYPE_CHOICES = [
        [RESOURCE_TYPE_CHOICES_IMAGE, 'image'],
        [RESOURCE_TYPE_CHOICES_VIDEO, 'video'],
    ]

    hidden = BooleanField(default=False, verbose_name=u'скрытная сущность')
    resource_type = PositiveSmallIntegerField(choices=RESOURCE_TYPE_CHOICES, null=True, blank=True)
    icon = ImageField(upload_to=upload_to_generate_filename, null=True, blank=True, verbose_name=u'иконка')

    objects = MainModelDefManager()
    admin_objects = MainModelDefAdminManager()
    admin_objects_objects = MainModelDefObjectsAdminManager()

    admin_exclude_fields = ['hidden', 'resource']

    class Meta:
        app_label = 'main'
        db_table = 'main_modeldefinition'
        ordering = ['id']
        verbose_name = u'модель'
        verbose_name_plural = u'модели'
