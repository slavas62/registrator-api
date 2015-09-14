# coding: utf-8
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from mutant.contrib.file.models import FilePathFieldDefinition
from mutant.contrib.related.models import ForeignKeyDefinition
from userlayers import get_modeldefinition_model
from userlayers.models import ModelDef as MD

ModelDef = get_modeldefinition_model()


@receiver(post_save, sender=MD, dispatch_uid='userlayers_admin')
def post_change(*args, **kwargs):
    wow = {
        'image': {'type': ModelDef.RESOURCE_TYPE_CHOICES_IMAGE, 'name': u'Изображение', 'name_plural': u'Изображения'},
        'video': {'type': ModelDef.RESOURCE_TYPE_CHOICES_VIDEO, 'name': u'Видео', 'name_plural': u'Видео'},
    }
    instance = kwargs.get('instance')
    if instance.name in wow or instance.hidden:
        return
    created = kwargs.get('created', None)
    if created:
        for w, wdata in wow.items():
            new = ModelDef(
                name='%ss_for_%s' % (w, instance.name), owner=instance.owner, resource_type=wdata['type'], hidden=True,
                verbose_name=wdata['name'], verbose_name_plural=wdata['name_plural'])
            new.save()
            ForeignKeyDefinition(
                name='object', model_def_id=new.contenttype_ptr_id, to_id=instance.contenttype_ptr_id,
                related_name='%ss' % w, verbose_name=instance.verbose_name).save()
            FilePathFieldDefinition(
                name='file', model_def_id=new.contenttype_ptr_id, path=settings.MEDIA_ROOT, recursive=True,
                verbose_name=u'файл').save()
