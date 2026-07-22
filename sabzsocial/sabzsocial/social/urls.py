from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import *

app_name = "social"

urlpatterns = [
    path('login' , auth_views.LoginView.as_view(authentication_form = LoginForm) , name = 'login'),
    path('logout' , views.log_out , name = 'logout'),
    path('profile' , views.profile , name = 'profile'),
    path('register' , views.register , name = 'register'),
    path('edit/' , views.edit_user , name = 'edit_user'),
    path('ticket/' , views.ticket , name = 'ticket'),
]