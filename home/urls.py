from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^profile/$', views.edit_user, name='profile'),
    url(r'^log/$', views.log_page, name='log_page'),
]
