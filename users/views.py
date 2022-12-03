from django.shortcuts import render
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.urls import reverse



# Create your views here.

def logout_view(request):
    """log out of page"""
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))

def register(request):
    """register the user and log the user in"""
    if request.method != 'POST':
    # no data submitted
        form = UserCreationForm()

    else:
    # data submitted
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('quizzes:index'))
    
    context = {'form': form}

    return render(request, 'users/register.html', context)        

