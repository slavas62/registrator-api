from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from userlayers.models import ModelDefinition


@receiver(post_delete, sender=ModelDefinition, dispatch_uid='userlayers_admin')
@receiver(post_save, sender=ModelDefinition, dispatch_uid='userlayers_admin')
def send(*args, **kwargs):
    from .admin import admin_modeldefinition_load
    admin_modeldefinition_load()
