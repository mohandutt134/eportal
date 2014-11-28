from django.conf.urls import patterns, include, url
from django.conf.urls import *
urlpatterns = patterns('quiz.views',
    # Examples:
    url(r'^quiz$', 'quiz', name='quiz'),
    url(r'^add_question$', 'add_question', name='add_question'),
    url(r'^attach_question$', 'attach_question', name='attach_question'),
    url(r'^quiz_confirm$', 'quiz_confirm', name='quiz_confirm'),
    url(r'^quiz_control$', 'quiz_control', name='quiz_control'),
    url(r'^edit_spec$', 'edit_spec', name='edit_spec'),
    url(r'^addquestion$', 'addquestion', name='addquestion'),
    url(r'^view_fullquestion$', 'view_fullquestion', name='view_fullquestion'),
    url(r'^removeQuestion$', 'removeQuestion', name='removeQuestion'),
    url(r'^qizquestions$', 'qizquestions', name='qizquestions'),

)
