from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.request_media, name='requestmedia'),
    url(r'^episodes/$', views.episodes, name='episodes'),
]
