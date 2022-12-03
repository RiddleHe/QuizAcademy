from . import views
from django.urls import re_path
from django.contrib.auth.views import LoginView

app_name = 'users'

urlpatterns = [
    # url for login
    re_path(r'^login/$', LoginView.as_view(template_name='users/login.html'), name='login'),
    # url for logout
    re_path(r'^logout/$', views.logout_view, name='logout'),
    # url for register
    re_path(r'^register/$', views.register, name='register'),
]