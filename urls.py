from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static

import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('myapp.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^payments/', include('getpaid.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
