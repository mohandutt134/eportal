from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf.urls import *
admin.autodiscover()

urlpatterns = patterns('student.views',
    # Examples:
    (r'^quizes/',include('quiz.urls')),
    (r'^',include('notification.urls')),
    url(r'^$', 'home', name='home'),
    url(r'^login/$', 'login_view', name='login'),
    url(r'^course$', 'courseView', name='courses'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    url(r'^faculty$', 'faculty', name='faculty'),
    url(r'^about$', 'about', name='about'),
    url(r'^logout$', 'logout_view', name='logout'),
    url(r'^reset/$', 'reset', name='reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$','reset_confirm', name='password_reset_confirm'),
    url(r'^success/$', 'success', name='success'),
    url(r'^edit/$', 'edit', name='edit'),
    url(r'^success2/$', 'success2', name='success2'),
    url(r'^fc/$', 'fc', name='fc'),
    #url('^inbox/notifications/', include(notifications.urls)),
)


