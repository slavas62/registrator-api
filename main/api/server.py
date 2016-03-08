from tastypie.resources import ModelResource

from userlayers.api.auth import FullAccessForLoginedUsers, Authentication
from main.models import Server


class ServerResource(ModelResource):
    class Meta:
        queryset = Server.objects.all()
        authorization = FullAccessForLoginedUsers()
        authentication = Authentication()

