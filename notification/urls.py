from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf.urls import *
admin.autodiscover()

urlpatterns = patterns('notification.views',
	url(r'^notificationicon_create$','notificationicon_create',name='notificationicon_create'),
	url(r'^notification_view/(?P<id>.*)/$','notification_view',name='notificationicon_view'),
	url(r'^message_view/(?P<dynamic_view_url>.*)/$','message_view',name='message_view'),
	)