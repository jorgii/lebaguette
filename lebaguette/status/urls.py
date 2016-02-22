from django.conf.urls import url

from . import views, ajax

urlpatterns = [
    url(r'^$', views.server_status, name='status'),
    url(r'^cpu/$', ajax.get_cpu_usage, name='cpu'),
    url(r'^temperatures/$', ajax.get_temperatures, name='temperatures'),
]
