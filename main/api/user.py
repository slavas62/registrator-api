from django.contrib.auth.models import User
from tastypie.resources import ModelResource

from userlayers.api.auth import FullAccessForLoginedUsers, Authentication


class CurrentUserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        authorization = FullAccessForLoginedUsers()
        authentication = Authentication()
        fields = ['id', 'email', 'first_name', 'last_name', 'username']

    def get_object_list(self, request):
        return super(CurrentUserResource, self).get_object_list(request).filter(id=request.user.id)
