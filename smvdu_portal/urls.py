from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf.urls import *
admin.autodiscover()

urlpatterns = patterns('student.views',
    # Examples:
    (r'^quizes/',include('quiz.urls')),
    #(r'^',include('notification.urls')),
    (r'^accounts/',include('accounts.urls')),
    url(r'^$', 'home', name='home'),
    url(r'^course$', 'courseView', name='courses'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    url(r'^faculty$', 'faculty', name='faculty'),
    url(r'^about$', 'about', name='about'),
    url(r'^edit/$', 'edit', name='edit'),
    url(r'^fc/$', 'fc', name='fc'),
    #url('^inbox/notifications/', include(notifications.urls)),
    url(r'^mail$','mail'),
    url(r'^change/$', 'changePassword', name='change'),
)


