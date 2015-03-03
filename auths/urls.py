from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'auths.views.home', name='home'),
    url(r'dashboard', 'auths.views.dashboard', name='dashboard'),
    # url(r'^blog/', include('blog.urls')),
)
