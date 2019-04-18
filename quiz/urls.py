from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.quiz_control, name='quiz_control'),
    url(r'^add_question$', views.add_question, name='add_question'),
    url(r'^attach_question/$', views.attach_question, name='attach_question'),
    url(r'^quiz_confirm$', views.quiz_confirm, name='quiz_confirm'),
    url(r'^edit_spec$', views.edit_spec, name='edit_spec'),
    url(r'^addquestion$', views.addquestion, name='addquestion'),
    url(r'^view_fullquestion$', views.view_fullquestion, name='view_fullquestion'),
    url(r'^removeQuestion$', views.removeQuestion, name='removeQuestion'),
    url(r'^qizquestions$', views.qizquestions, name='qizquestions'),
    url(r'^EditQuiz$', views.EditQuiz, name='EditQuiz'),
    url(r'^changeQuiz$', views.changeQuiz, name='changeQuiz'),
    url(r'^exit/$', views.exit, name='exit'),
    url(r'^courses/(?P<id>[0-9A-Za-z_\-]+)/create_course_quiz$', views.create_course_quiz, name='create_course_quiz'),
    url(r'^course/(?P<id>[0-9A-Za-z_\-]+)/course_quiz$', views.course_quiz, name='course_quiz'),
    url(r'^courses/(?P<course_id>[0-9A-Za-z_\-]+)/course_quiz/(?P<quiz_id>[0-9A-Za-z_\-]+)/$', views.quiz_view,
        name='quiz_view'),
    url(r'^quiz_questions/$', views.quiz_questions, name='quiz_questions'),
    url(r'^submit/$', views.submit, name='submi'),
    url(r'^quiz_result/$', views.quiz_result, name='quiz_result'),
    url(r'^quizresult/(?P<course>[0-9A-Za-z_\-]+)$', views.show_result, name='show_result'),

]
