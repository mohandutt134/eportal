from django.conf.urls import url
from views import login_view, logout_view, register2, reset, success, success2, lock, reset_confirm

urlpatterns = [
    url(r'^login/$', login_view, name='login'),
    url(r'^register/$', register2, name='register2'),
    url(r'^logout$', logout_view, name='logout'),
    url(r'^reset/$', reset, name='reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        reset_confirm, ),
    url(r'^success/$', success, name='success'),
    url(r'^success2/$', success2, name='success2'),
    url(r'^lock/$', lock, ),
]
