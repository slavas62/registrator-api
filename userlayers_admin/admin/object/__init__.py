# coding: utf-8
from django.contrib.gis.admin import OSMGeoAdmin


class OSMAdmin(OSMGeoAdmin):
    debug = True


class ModelDefinitionObjectAdmin(OSMAdmin):
    suit_form_tabs = [
        ['general', u'Основные св-ва'],
    ]
