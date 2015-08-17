# coding: utf-8

from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy
from .views import LoginView

urlpatterns = patterns(
    '',
    url(r'^login/$', LoginView.as_view(success_url='/secret_admin_zone'), name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'acc/logout.html', 'next_page': '/'}, name='logout'),
)
