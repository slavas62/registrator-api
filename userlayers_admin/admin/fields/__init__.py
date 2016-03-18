# coding: utf-8
from userlayers.forms import FIELD_TYPES
from userlayers_admin.admin.fields.base import FieldAdmin
from userlayers_admin.admin.fields.foreign_key import ForeignKeyFieldAdmin

FIELD_TYPES_ADMIN_CLASS = dict((k, FieldAdmin) for k, v in FIELD_TYPES)
FIELD_TYPES_ADMIN_CLASS['foreign_key'] = ForeignKeyFieldAdmin
