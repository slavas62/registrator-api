# coding: utf-8
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

SETTINGS_USERLAYERS_ADMIN_MD_OBJECT_CLASS = 'USERLAYERS_ADMIN_MD_OBJECT_CLASS'
USERLAYERS_ADMIN_MD_OBJECT_CLASS_DEFAULT = 'userlayers_admin.admin.object.ModelDefinitionObjectAdmin'
USERLAYERS_ADMIN_MD_OBJECT_CLASS = getattr(
    settings, SETTINGS_USERLAYERS_ADMIN_MD_OBJECT_CLASS, USERLAYERS_ADMIN_MD_OBJECT_CLASS_DEFAULT)


def get_objects_admin_class():
    def import_class(cl):
        d = cl.rfind(".")
        classname = cl[d + 1:len(cl)]
        m = __import__(cl[0:d], globals(), locals(), [classname])
        return getattr(m, classname)

    try:
        return import_class(USERLAYERS_ADMIN_MD_OBJECT_CLASS)
    except AttributeError as e:
        raise ImproperlyConfigured("%s class doesn't exists" % USERLAYERS_ADMIN_MD_OBJECT_CLASS)
