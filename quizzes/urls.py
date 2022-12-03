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
    
]