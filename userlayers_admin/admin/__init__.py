# coding: utf-8
from django.db import ProgrammingError
from django.contrib import admin
from userlayers import get_modeldefinition_model
from userlayers_admin.admin.modeldefinition import ModelDefinitionAdmin
from userlayers_admin.admin.builder import ModelDefinitionAdminBuilder
from userlayers_admin.admin.object.admin_class import get_modeldefinition_admin_class

ModelDef = get_modeldefinition_model()

admin.site.register(ModelDef, get_modeldefinition_admin_class())

builder = ModelDefinitionAdminBuilder()
# catch syncdb exception
try:
    builder.build()
except ProgrammingError as e:
    pass


from userlayers_admin.admin.fields_choices import *
