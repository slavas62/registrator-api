from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from userlayers.models import ModelDefinition


@receiver(pre_delete, sender=ModelDefinition, dispatch_uid='userlayers_admin')
@receiver(pre_save, sender=ModelDefinition, dispatch_uid='userlayers_admin')
def pre_change(*args, **kwargs):
    from .admin import admin_modeldefinition_unload
    admin_modeldefinition_unload()


@receiver(post_delete, sender=ModelDefinition, dispatch_uid='userlayers_admin')
@receiver(post_save, sender=ModelDefinition, dispatch_uid='userlayers_admin')
def post_change(*args, **kwargs):
    from .admin import admin_modeldefinition_load
    admin_modeldefinition_load()
