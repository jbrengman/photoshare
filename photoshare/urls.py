from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import photoshare_app.urls

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^photoshare/', include(photoshare_app.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
