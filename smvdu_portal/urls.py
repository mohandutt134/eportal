from django.conf.urls import patterns, include, url
from . import settings
from django.contrib import admin
from django.conf.urls import *
admin.autodiscover()

urlpatterns = patterns('student.views',
    # Examples:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^attendance/', include('attendance.urls')),
    #(r'^markdown/', include("django_markdown.urls")),
    (r'^quiz/',include('quiz.urls')),
    (r'online/',include('online_status.urls')),
    (r'^notification/',include('notification.urls')),
    (r'^accounts/',include('accounts.urls')),
    #(r'^report/',include('report.urls')),
    url(r'^$', 'home', name='home'),
    url(r'^dashboard$', 'dashboard', name='dashboard'),
   
    url(r'^courses/(?P<id>[0-9A-Za-z_\-]+)$', 'course', name='course'),
    url(r'^courses$', 'courses', name='courses'),
    url(r'^profile$', 'profile', name='profile'),

    url(r'^profile/(?P<username>[0-9A-Za-z_\-]+)$',  'pprofile', name='pprofile'),
    url(r'^users/(?P<username>[0-9A-Za-z_\-]+)/$',  'pprofile', name='pprofile'),

    url(r'^about$', 'about', name='about'),
    #url(r'^profile_edit/$', 'profile_edit', name='profile_edit'),
    #url('^inbox/notifications/', include(notifications.urls)),
    url(r'^mail$','mail'),
    url(r'^change/$', 'changePassword', name='change'),

    url(r'^courses/(?P<id>[0-9A-Za-z_\-]+)/addmaterial$', 'add_material', name='add_material'),
    url(r'^allcourses$', 'allcourses', name='allcourses'),
    url(r'^courseinfo/(?P<id>[0-9A-Za-z_\-]+)$','course_info',name='course_info'),
    url(r'^faculty$', 'faculties', name='faculty'),

    url(r'^test$', 'test', name='test'),

)

if settings.DEBUG is False:   #if DEBUG is True it will be served automatically
    urlpatterns += patterns('',
            url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

urlpatterns += patterns('',
            url(r'^pdf/(?P<username>[0-9A-Za-z_\-]+)$', 'student.genpdf.myview', name='pdf'),
    )
