from django.contrib import admin
from django.conf.urls import *
from student import views

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^attendance/', include('attendance.urls')),
    url(r'^quiz/', include('quiz.urls')),
    url(r'^notification/', include('notification.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^$', views.home, name='home'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^contact$', views.contactview, name='contact'),
    url(r'^faculty$', views.faculties, name='faculty'),
    url(r'^about$', views.about, name='about'),
    url(r'^allcourses$', views.allcourses, name='allcourses'),
    url(r'^courses/(?P<id>[0-9A-Za-z_\-]+)$', views.course, name='course'),
    url(r'^courses$', views.courses, name='courses'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^profile/(?P<username>[0-9A-Za-z_\-\.]+)$', views.pprofile, name='pprofile'),
    url(r'^users/(?P<username>[0-9A-Za-z_\-\.]+)/$', views.pprofile, name='pprofile'),

    # # url(r'^profile_edit/$', 'profile_edit', name='profile_edit'),
    # # url('^inbox/notifications/', include(notifications.urls)),
    # url(r'^mail$', 'mail'),
    # url(r'^change/$', 'changePassword', name='change'),
    #
    # url(r'^courses/(?P<id>[0-9A-Za-z_\-]+)/addmaterial$', 'add_material', name='add_material'),
    # url(r'^courseinfo/(?P<id>[0-9A-Za-z_\-]+)$', 'course_info', name='course_info'),
    # url(r'^courseregister/$', 'course_register', name='course_register'),
    # # (r'^ckeditor/', include('ckeditor.urls')),
    url(r'^addann/$', views.add_ann, name='addann'),
    url(r'^addvideo/$', views.add_video, name='addvideo'),
    #
    # url(r'^addsyllabus/(?P<id>[0-9A-Za-z_\-]+)$$', 'add_syllabus', name='addsyllabus'),
]
