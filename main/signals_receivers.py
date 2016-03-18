# coding: utf-8
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from mutant.contrib.file.models import FilePathFieldDefinition
from mutant.contrib.related.models import ForeignKeyDefinition
from userlayers import get_modeldefinition_model
from userlayers.models import ModelDef as MD

ModelDef = get_modeldefinition_model()


@receiver(post_save, sender=MD, dispatch_uid='registreator')
def post_change(*args, **kwargs):
    wow = {
        'image': {'type': ModelDef.RESOURCE_TYPE_CHOICES_IMAGE, 'name': u'Изображение', 'name_plural': u'Изображения'},
        'video': {'type': ModelDef.RESOURCE_TYPE_CHOICES_VIDEO, 'name': u'Видео', 'name_plural': u'Видео'},
    }
    instance = kwargs.get('instance')
    if instance.name in wow or instance.hidden:
        return
    if kwargs.get('created', None):
        ForeignKeyDefinition(
            name='user', model_def_id=instance.contenttype_ptr_id, related_name='%ss' % instance.name,
            to_id=ContentType.objects.get_for_model(get_user_model()).id,
            verbose_name=u'владелец').save()
        for name, data in wow.items():
            inline = ModelDef(
                name='%ss_for_%s' % (name, instance.name), owner=instance.owner, resource_type=data['type'],
                hidden=True, verbose_name=data['name'], verbose_name_plural=data['name_plural'])
            inline.save()
            ForeignKeyDefinition(
                name='object', model_def_id=inline.contenttype_ptr_id, to_id=instance.contenttype_ptr_id,
                related_name='%ss' % name, verbose_name=instance.verbose_name).save()
            FilePathFieldDefinition(
                name='file', model_def_id=inline.contenttype_ptr_id, path=settings.MEDIA_ROOT, recursive=True,
                verbose_name=u'файл').save()


@receiver(post_delete, sender=MD, dispatch_uid='registreator')
def post_delete(instance, *args, **kwargs):
    for inline in ModelDef.objects.filter(
            hidden=True,
            name__icontains='for_%s' % instance.name,
            resource_type__in=dict(ModelDef.RESOURCE_TYPE_CHOICES).keys()
    ):
        inline.delete()
