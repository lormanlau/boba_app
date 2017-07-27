from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^dashboard$', views.dashboard),
	url(r'^addplace$', views.addplace),
	url(r'^register$', views.register),
	url(r'^login$', views.dashboard),
	url(r'^getall', views.getall),
	url(r'^profile/(?P<user_id>\d+)$', views.profile),
	url(r'^signin$', views.signin),
	url(r'^reg$', views.reg),

]