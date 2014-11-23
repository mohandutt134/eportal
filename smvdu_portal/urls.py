from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf.urls import *
admin.autodiscover()

urlpatterns = patterns('student.views',
    # Examples:
    (r'^admin/', include(admin.site.urls)),
    (r'^markdown/', include("django_markdown.urls")),
    (r'^quizes/',include('quiz.urls')),
    (r'online/',include('online_status.urls')),
    #(r'^',include('notification.urls')),
    (r'^accounts/',include('accounts.urls')),
    url(r'^$', 'home', name='home'),
    url(r'^dashboard$', 'dashboard', name='dashboard'),
    url(r'^course$', 'courseView', name='courses'),
    url(r'^add_question$', 'add_question', name='add_question'),
    url(r'^attach_question$', 'attach_question', name='attach_question'),
    url(r'^quiz_confirm$', 'quiz_confirm', name='quiz_confirm'),
    url(r'^quiz_control$', 'quiz_control', name='quiz_control'),
    url(r'^edit_spec$', 'edit_spec', name='edit_spec'),
    url(r'^addmaterial$', 'addmaterial', name='addmaterial'),
    url(r'^admin_course_view$', 'admin_course_view', name='admin_course_view'),
    url(r'^admin_courses$', 'admin_courses', name='admin_courses'),
    #url(r'^attendance$', 'attendance', name='attendance'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    url(r'^faculty$', 'faculty', name='faculty'),
    url(r'^about$', 'about', name='about'),
    url(r'^edit/$', 'edit', name='edit'),
    url(r'^fc/$', 'fc', name='fc'),
    #url('^inbox/notifications/', include(notifications.urls)),
    url(r'^mail$','mail'),
    url(r'^change/$', 'changePassword', name='change'),
)


