from django.conf.urls import url

from . import views, ajax

urlpatterns = [
    url(r'^$', views.server_status, name='status'),
    url(r'^cpu$', ajax.get_cpu_usage, name='cpu'),
    url(r'^ram$', ajax.get_ram_usage, name='ram'),
    url(r'^disk_data$', ajax.get_disk_data, name='disk_data'),
    url(r'^disk_usage$', ajax.get_disk_usage, name='disk_usage'),
    url(r'^uptime$', ajax.get_uptime, name='uptime'),
    url(r'^service/(?P<servicename>.+)/$', ajax.get_service, name='service'),
]
