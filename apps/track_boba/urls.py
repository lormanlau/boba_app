from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^dashboard$', views.dashboard),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^getall', views.getall),
	url(r'^profile/(?P<user_id>\d+)$', views.profile),
	url(r'^logout$', views.logout),
	url(r'^search$', views.search),
	url(r'^add_friend/(?P<user_id>\d+)$', views.add_friend),
	url(r'^addboba$', views.addboba)
]