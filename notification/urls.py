from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^notification_create$', views.notification_create, name='notification_create'),
    url(r'^notification_view/(?P<id>.*)/$', views.notification_view, name='notification_view'),
    url(r'^message_view/$', views.message_view, name='message_view'),
    url(r'^all_notification/$', views.all_notification, name='all_notification'),
    url(r'^bulk_message/(?P<id>.*)/$', views.bulk_message, name='bulk_message'),
    url(r'^messageToFaculty/(?P<email>.*)/$', views.messageToFaculty, name='messageToFaculty'),
]
