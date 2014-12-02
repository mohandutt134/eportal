from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf.urls import *
admin.autodiscover()

urlpatterns = patterns('notification.views',
	url(r'^notificationicon_create$','notificationicon_create',name='notificationicon_create'),
	url(r'^notification_view/(?P<id>.*)/$','notification_view',name='notificationicon_view'),
	url(r'^message_view/$','message_view',name='message_view'),
	url(r'^all_notification/$','all_notification',name='all_notification'),
	url(r'^bulk_message/(?P<id>.*)/$','bulk_message',name='bulk_message'),
	url(r'^messageToFaculty/(?P<email>.*)/$','messageToFaculty',name='messageToFaculty'),
	)