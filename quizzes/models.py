from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):

    curr_question = models.CharField(max_length=200, null=True)
    op1 = models.CharField(max_length=200, null=True)
    op2 = models.CharField(max_length=200, null=True)
    op3 = models.CharField(max_length=200, null=True)
    op4 = models.CharField(max_length=200, null=True)
    answer = models.CharField(max_length=200, null=True)
    next_question = models.ForeignKey(to='Question', null=True, blank=True, on_delete=models.SET_NULL, related_name='next')
    prev_question = models.ForeignKey(to='Question', null=True, blank=True, on_delete=models.SET_NULL, related_name='prev')

    def __str__(self):
        return self.curr_question

class Quiz(models.Model):

    name = models.CharField(max_length=100)
    head = models.ForeignKey(Question, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Score(models.Model):

    created_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)
    correct = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    percentage = models.IntegerField(default=0)
    quiz = models.ForeignKey(Quiz, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return "Score"

