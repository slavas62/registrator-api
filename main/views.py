from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm


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
    return HttpResponse('')


@csrf_exempt
def logout_view(request, *args, **kwargs):
    auth_logout(request)
    return HttpResponse('')
