from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf.urls import *
admin.autodiscover()

urlpatterns = patterns('notification.views',
	url(r'^notificationicon_create$','notificationicon_create',name='notificationicon_create'),
	)