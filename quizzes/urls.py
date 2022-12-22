from . import views
from django.urls import path,re_path

app_name = 'quzzes'

urlpatterns = [
    path('', views.index, name='index'),
    # for the page that opens a quiz
    re_path('^quiz/(?P<quiz_id>\d+)/$', views.quiz, name='quiz'),
    # for the individual questions
    re_path('^question/(?P<question_id>\d+)/$', views.question, name='question'),
    # for the result of the quiz
    re_path('^result/$', views.result, name='result'),
    # for adding questions
    re_path('^add_question/(?P<quiz_id>\d+)/$', views.add_question, name='add_question'),
    # for adding quizzes
    re_path('^add_quiz/$', views.add_quiz, name='add_quiz'),
    # for editing questions
    re_path('^edit_quiz/$', views.edit_quiz, name='edit_quiz'),
]