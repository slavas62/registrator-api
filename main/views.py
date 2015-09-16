from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import View


@csrf_exempt
def login_view(request, *args, **kwargs):
    authentication_form = AuthenticationForm
    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return HttpResponse('')
        else:
            return HttpResponseForbidden('')
    if request.method == "GET":
        return HttpResponse('''<form method="post">
        <input type="text" name="username"/><input type="password" name="password"/>
        <input type="submit"/></form>''')
    return HttpResponseBadRequest('')


@csrf_exempt
def logout_view(request, *args, **kwargs):
    auth_logout(request)
    return HttpResponse('')


class TokenGetView(View):
    def dispatch(self, request, *args, **kwargs):
        return HttpResponse(get_token(request))
