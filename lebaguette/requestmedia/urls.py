from django.conf.urls import url

from . import views, ajax

urlpatterns = [
    url(r'^$', views.request_media, name='requestmedia'),
    url(r'^complete/$', ajax.mark_episode_complete, name='complete'),
]
