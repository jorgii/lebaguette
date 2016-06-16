from django.conf.urls import url

from . import views, ajax

urlpatterns = [
    url(r'^$', views.request_media, name='requestmedia'),
    url(r'^approved$', views.approved_media, name='approved_media'),
    url(r'^rejected$', views.rejected_media, name='rejected_media'),
    url(r'^completed$', views.completed_media, name='completed_media'),
    url(r'^complete/$', ajax.mark_request_complete, name='complete'),
]
