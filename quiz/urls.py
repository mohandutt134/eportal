from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^quiz$', 'quiz.views.quiz', name='quiz'),

)