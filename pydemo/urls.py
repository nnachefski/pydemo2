#add URL mapping here

from django.conf.urls import url
from django.contrib import admin
from django.conf import settings

from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'(.+\.html)$', 'direct_to_template'),
    url(r'^$', views.index, name='index'),
    url(r'^test$', views.test),
    url(r'^dt', views.dt),
    url(r'^env', views.env),
    url(r'^proc', views.proc),
    url(r'^file', views.file),
    url(r'^verb', views.verb),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + [url(r'^.+', views.none)]