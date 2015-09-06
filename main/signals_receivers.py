from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from mutant.models import FieldDefinition, ModelDefinition as MD
from userlayers.models import ModelDefinition

@receiver(post_save, sender=MD, dispatch_uid='userlayers_admin')
@receiver(post_delete, sender=MD, dispatch_uid='userlayers_admin')
@receiver(post_save, sender=ModelDefinition, dispatch_uid='userlayers_admin')
@receiver(post_delete, sender=ModelDefinition, dispatch_uid='userlayers_admin')
@receiver(post_save, sender=FieldDefinition, dispatch_uid='userlayers_admin')
@receiver(post_delete, sender=FieldDefinition, dispatch_uid='userlayers_admin')
def post_change(*args, **kwargs):
    from main.admin import builder
    builder.build()
