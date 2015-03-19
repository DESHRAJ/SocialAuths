from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'', include('auths.urls')),
    (r'logout', 'django.contrib.auth.views.logout',{'next_page': '/'}),
    (r'', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
