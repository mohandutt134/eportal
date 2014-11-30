from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf.urls import *
admin.autodiscover()

urlpatterns = patterns('attendance.views',
	url(r'^makeattendence$','show_students',name='show_students'),
	url(r'^index$','controls',name='controls'),
	url(r'^showattendence$','show',name='show'),
	)