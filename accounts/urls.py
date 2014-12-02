from django.conf.urls import patterns, include, url
import notifications
from django.conf.urls import *

urlpatterns = patterns('accounts.views',
    # Examples:
    
    url(r'^login/$', 'login_view', name='login'),
    url(r'^register/$', 'register2', name='register2'),
    url(r'^logout$', 'logout_view', name='logout'),
    url(r'^reset/$', 'reset', name='reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$','reset_confirm', name='password_reset_confirm'),
    url(r'^success/$', 'success', name='success'),
    url(r'^success2/$', 'success2', name='success2'),
    url(r'^lock/$', 'lock', name='lock'),
    url(r'^change_password/$','change_password',name='change_password'),


)