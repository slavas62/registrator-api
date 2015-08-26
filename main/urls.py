# coding: utf-8
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = [
    url('^$', RedirectView.as_view(url='/secret_admin_zone', permanent=False)),
    url(r'^secret_admin_zone/', include(admin.site.urls)),
    # url(r'^acc/', include('acc.urls')),
    url(r'^userlayers/', include('userlayers.urls')),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
