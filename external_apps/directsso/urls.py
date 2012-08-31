from django.conf.urls.defaults import *

urlpatterns = patterns('directsso.views',
    url(r'^$', 'handle_auth', name="sso-handle-auth"),
)
