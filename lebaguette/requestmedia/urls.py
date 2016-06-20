from django.conf.urls import url

from . import views, ajax

urlpatterns = [
    url(r'^$', views.request_media, name='requestmedia'),
    url(r'^approved$', views.approved_media, name='approved_media'),
    url(r'^rejected$', views.rejected_media, name='rejected_media'),
    url(r'^completed$', views.completed_media, name='completed_media'),
    url(r'^complete/$', ajax.complete_request, name='complete_request'),
    url(r'^approve/$', ajax.approve_request, name='approve_request'),
    url(r'^reject/$', ajax.reject_request, name='reject_request'),
    url(r'^add/$', ajax.add_request, name='add_request'),
]
