from django.conf.urls import patterns, include, url
import notifications
from django.contrib import admin
from django.conf.urls import *
admin.autodiscover()

urlpatterns = patterns('student.views',
    # Examples:
    (r'^quizes/',include('quiz.urls')),
    url(r'^$', 'home', name='home'),
    url(r'^login/$', 'login_view', name='login'),
    url(r'^course$', 'courseView', name='courses'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    url(r'^faculty$', 'faculty', name='faculty'),
    url(r'^about$', 'about', name='about'),
    url(r'^logout$', 'logout_view', name='logout'),
    url(r'^reset/$', 'reset', name='reset'),
    url(r'^all/$', 'all', name='all'),
    url(r'^unread/$', 'unread', name='unread'),
    url(r'^mark-all-as-read/$', 'mark_all_as_read', name='mark_all_as_read'),
    url(r'^mark-as-read/(?P<slug>\d+)/$', 'mark_as_read', name='mark_as_read'),
    url(r'^mark-as-unread/(?P<slug>\d+)/$', 'mark_as_unread', name='mark_as_unread'),
    url(r'^delete/(?P<slug>\d+)/$', 'delete', name='delete'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$','reset_confirm', name='password_reset_confirm'),
    url(r'^success/$', 'success', name='success'),
    url(r'^edit/$', 'edit', name='edit'),
    url(r'^success2/$', 'success2', name='success2'),
    url(r'^fc/$', 'fc', name='fc'),
    url('^inbox/notifications/', include(notifications.urls)),
)


