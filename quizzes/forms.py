from django.forms import ModelForm
from .models import Question, Quiz
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AddQuestion(ModelForm):
    class Meta:
        model=Question
        fields=['curr_question', 'op1', 'op2', 'op3', 'op4', 'answer']
        labels={'curr_question': 'Question', 'op1': 'Option 1', 'op2': 'Option 2', 'op3': 'Option3', 'op4': 'Option 4'}

class AddQuiz(ModelForm):
    class Meta:
        model=Quiz
        fields=['name']
        labels={'name': 'Name'}

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username', 'password']