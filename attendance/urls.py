from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^makeattendence$', views.show_students, name='show_students'),
    url(r'^index$', views.controls, name='controls'),
    url(r'^showattendence$', views.show, name='show'),
]
