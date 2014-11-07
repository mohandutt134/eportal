from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^index$', 'student.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^login$', 'student.views.login', name='login'),
    url(r'^course$', 'course.views.course', name='login'),
    url(r'^admin/', include(admin.site.urls)),
)
