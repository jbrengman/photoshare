from django.conf.urls import patterns, url
from django.contrib import admin
from django.http import HttpResponse

admin.autodiscover()

urlpatterns = patterns(
    'photoshare_app.views',
    url(r'^$', 'home_view', name='home'),
    url(r'^(\w+)/album/(\d+)/$', 'album_view', name='album'),
    url(r'^(\w+)/albums/$', 'albums_view', name='albums'),
    url(r'^photo/(\d+)/$', 'photo_view', name='photo'),
    url(r'^tag/(\w+)/$', 'tag_view', name='tag'),
    url(r'^login/$', 'login_view', name='login'),
    url(r'^logout/$', 'logout_view', name='logout'),
    url(r'^register/$', 'register_view', name='register'),
)


def stub_view(request, *args, **kwargs):
    body = "Stub View\n\n"
    if args:
        body += "Args:\n"
        body += "\n".join(["\t%s" % a for a in args])
    if kwargs:
        body += "Kwargs:\n"
        body += "\n".join(["\t%s: %s" % i for i in kwargs.items()])
    return HttpResponse(body, content_type="text/plain")
