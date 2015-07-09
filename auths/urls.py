from django.conf.urls import patterns, include, url
from auths.views import AddStorage
urlpatterns = patterns('',
    # url(r'temp1', 'auths.views.temp1', name='temp1'),        
    # url(r'^blog/', include('blog.urls')),
    # url(r'temp', 'auths.views.temp', name='temp'),
    url(r'^$', 'auths.views.home', name='home'),
    url(r'testaclass', 'auths.views.testaclass', name='testaclass'),
    url(r'trainclass', 'auths.views.trainModel', name='trainModel'),
    url(r'deleteimage', 'auths.views.deleteImage', name='deleteImage'),
    url(r'dashboard', 'auths.views.dashboard', name='dashboard'),
    url(r'material', 'auths.views.material', name='material'),
    url(r'^addstorage/$', 'auths.views.storage', name='addstorage'),
    # url(r's3connect', 'auths.views.s3connect', name='s3connect'),
    url(r'apitest', 'auths.views.storage_api', name='apitest'),
)
