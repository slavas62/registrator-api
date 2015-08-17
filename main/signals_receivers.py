from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete, post_delete, pre_save, m2m_changed
from mutant.models import ModelDefinition, BaseDefinition, UniqueTogetherDefinition, FieldDefinition


@receiver(pre_delete, sender=ModelDefinition, dispatch_uid='userlayers.path')
@receiver(post_delete, sender=ModelDefinition, dispatch_uid='userlayers.path')
@receiver(pre_save, sender=ModelDefinition, dispatch_uid='userlayers.path')
@receiver(post_save, sender=ModelDefinition, dispatch_uid='userlayers.path')
@receiver(pre_delete, sender=BaseDefinition, dispatch_uid='userlayers.path')
@receiver(post_delete, sender=BaseDefinition, dispatch_uid='userlayers.path')
@receiver(pre_save, sender=BaseDefinition, dispatch_uid='userlayers.path')
@receiver(post_save, sender=BaseDefinition, dispatch_uid='userlayers.path')
@receiver(m2m_changed, sender=UniqueTogetherDefinition.field_defs.through, dispatch_uid='userlayers.path')
@receiver(pre_delete, sender=FieldDefinition, dispatch_uid='userlayers.path')
@receiver(post_delete, sender=FieldDefinition, dispatch_uid='userlayers.path')
@receiver(pre_save, sender=FieldDefinition, dispatch_uid='userlayers.path')
@receiver(post_save, sender=FieldDefinition, dispatch_uid='userlayers.path')
def send(*args, **kwargs):
    from .admin import admin_modeldefinition_load
    admin_modeldefinition_load()
