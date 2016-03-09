# coding: utf-8
from django.conf import settings
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from main.api import v1_api
from main.views import TokenGetView

admin.autodiscover()

urlpatterns = [
    url('^$', RedirectView.as_view(url='/secret_admin_zone', permanent=False)),
    url(r'^get-token/$', TokenGetView.as_view(), name='token-get'),
    url(r'^secret_admin_zone/', include(admin.site.urls)),
    # url(r'^acc/', include('acc.urls')),
    url(r'^userlayers/api/', include(v1_api.urls)),
    url(r'^login/', 'main.views.login_view', name='login'),
    url(r'^logout/', 'main.views.logout_view', name='logout'),
    url(r'^is-authenticated/', 'main.views.is_authenticated_view', name='is-authenticated'),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
