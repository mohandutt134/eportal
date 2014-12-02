from django.conf.urls import patterns, include, url
from django.conf.urls import *
urlpatterns = patterns('quiz.views',
    # Examples:
    url(r'^quiz$', 'quiz', name='quiz'),
    url(r'^add_question$', 'add_question', name='add_question'),
    url(r'^attach_question/$', 'attach_question', name='attach_question'),
    url(r'^quiz_confirm$', 'quiz_confirm', name='quiz_confirm'),
    url(r'^quiz_control$', 'quiz_control', name='quiz_control'),
    url(r'^edit_spec$', 'edit_spec', name='edit_spec'),
    url(r'^addquestion$', 'addquestion', name='addquestion'),
    url(r'^view_fullquestion$', 'view_fullquestion', name='view_fullquestion'),
    url(r'^removeQuestion$', 'removeQuestion', name='removeQuestion'),
    url(r'^qizquestions$', 'qizquestions', name='qizquestions'),
    url(r'^EditQuiz$', 'EditQuiz', name='EditQuiz'),
    url(r'^changeQuiz$', 'changeQuiz', name='changeQuiz'),
    url(r'^exit/$', 'exit', name='exit'),
    url(r'^courses/(?P<id>[0-9A-Za-z_\-]+)/create_course_quiz$', 'create_course_quiz', name='create_course_quiz'),
    url(r'^course/(?P<id>[0-9A-Za-z_\-]+)/course_quiz$', 'course_quiz', name='course_quiz'),
    url(r'^courses/(?P<course_id>[0-9A-Za-z_\-]+)/course_quiz/(?P<quiz_id>[0-9A-Za-z_\-]+)/$', 'quiz_view', name='quiz_view'),
    url(r'^quiz_questions/$','quiz_questions',name='quiz_questions'),
    url(r'^submit/$','submit',name='submi'),
    url(r'^quiz_result/$','quiz_result',name='quiz_result'),

)
