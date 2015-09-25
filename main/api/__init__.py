# coding: utf-8
from tastypie.api import Api
from main.api.table_proxy import TableProxyResource
from userlayers.api.resources import TablesResource, FieldsResource, FileImportResource

v1_api = Api(api_name='v1')
v1_api.register(TablesResource())
v1_api.register(FieldsResource())
v1_api.register(TableProxyResource())
v1_api.register(FileImportResource())