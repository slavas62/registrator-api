from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from mutant.models import FieldDefinition, ModelDefinition as MD
from userlayers import get_modeldefinition_model
from userlayers_admin.contrib.request_middleware import get_request_installed, get_request

ModelDef = get_modeldefinition_model()


@receiver(post_save, sender=MD, dispatch_uid='userlayers_admin')
@receiver(post_delete, sender=MD, dispatch_uid='userlayers_admin')
@receiver(post_save, sender=ModelDef, dispatch_uid='userlayers_admin')
@receiver(post_delete, sender=ModelDef, dispatch_uid='userlayers_admin')
@receiver(post_save, sender=FieldDefinition, dispatch_uid='userlayers_admin')
@receiver(post_delete, sender=FieldDefinition, dispatch_uid='userlayers_admin')
def post_change(*args, **kwargs):
    if get_request_installed() and not get_request():
        return
    from userlayers_admin.admin import builder
    builder.build()
