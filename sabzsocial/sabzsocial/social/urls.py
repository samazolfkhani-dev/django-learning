from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import *
from django.urls import reverse_lazy

app_name = "social"

urlpatterns = [
    path('login' , auth_views.LoginView.as_view(authentication_form = LoginForm) , name = 'login'),
    path('logout' , views.log_out , name = 'logout'),
    path('profile/' , views.profile , name = 'profile'),
    path('register' , views.register , name = 'register'),
    path('edit/' , views.edit_user , name = 'edit_user'),
    path('ticket/' , views.ticket , name = 'ticket'),
    path('password_change/' , auth_views.PasswordChangeView.as_view(success_url = reverse_lazy('social:password_change_done')) , name = 'password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view() , name = 'password_change_done'),
    path('password_reset/' , auth_views.PasswordResetView.as_view(success_url = reverse_lazy('social:password_reset_done')) , name = 'password_reset'),
    path('password_reset/done/' , auth_views.PasswordResetDoneView.as_view() , name = 'password_reset_done'),
    path('password_reset/<uidb64>/<token>/' , auth_views.PasswordResetConfirmView.as_view(success_url = reverse_lazy('social:password_reset_complete')) , name = 'password_reset_confirm'),
    path('password_reset/complete' , auth_views.PasswordResetCompleteView.as_view() , name = 'password_reset_complete'),
    path('posts/' , views.post_list , name = "post_list"),
    path('posts/post/<slug:tag_slug>/' , views.post_list , name = "post_list_by_tag"),
    path('posts/create_post' , views.create_post , name = 'create_post'),
    path('posts/detail/<int:post_id>' , views.post_detail , name='post_detail'),
    path('posts/<int:id>/comments' , views.post_comment, name = 'post_comment' ),
    path('edit_post/<post_id>' , views.edit_post , name = 'edit_post'),
    path('delete_post/<post_id>' , views.delete_post , name = 'delete_post')
]