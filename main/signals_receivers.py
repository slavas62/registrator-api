from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from mutant.models import ModelDefinition, BaseDefinition


@receiver(post_delete, sender=ModelDefinition, dispatch_uid='userlayers.path')
@receiver(post_save, sender=ModelDefinition, dispatch_uid='userlayers.path')
@receiver(post_delete, sender=BaseDefinition, dispatch_uid='userlayers.path')
@receiver(post_save, sender=BaseDefinition, dispatch_uid='userlayers.path')
def send(*args, **kwargs):
    from .admin import admin_modeldefinition_load
    admin_modeldefinition_load()
