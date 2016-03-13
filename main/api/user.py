from django.contrib.auth.models import User
from tastypie.resources import ModelResource

from userlayers.api.auth import FullAccessForLoginedUsers, Authentication


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        authorization = FullAccessForLoginedUsers()
        authentication = Authentication()
        fields = ['id', 'email', 'first_name', 'last_name', 'username']

    def get_object_list(self, request):
        qs = super(UserResource, self).get_object_list(request)
        if not request.user.is_superuser:
            return qs.filter(id=request.user.id)
        return qs
