from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^index$', 'student.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
     url(r'^login$', 'student.views.login', name='login'),
     url(r'^courses$', 'student.views.courses', name='courses'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^faculty$', 'student.views.faculty', name='faculty'),
    url(r'^about$', 'smvdu_portal.views.about', name='about'),
   
    
)
