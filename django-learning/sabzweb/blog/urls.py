from django.urls import path
from . import views

app_name = "blog"

urlpatterns =  [
    path('' , views.index , name = 'index'),
    # path('posts/' , views.post_list , name = 'post_list'),
    path('posts/' , views.PostListView.as_view() , name = 'posts'),
    path('posts/<int:id>' , views.post_detail , name = 'post_detail'),
    # path('posts/<pk>' , views.PostDetailView.as_view() , name = 'post_detail'),
    path('posts/<int:id>/comments' , views.post_comment, name = 'post_comment' ),
    path('ticket/' , views.ticket , name = 'ticket'),
    path('post/' , views.post_form , name = 'post_form'),
    path('search' , views.post_search , name = 'post_search'),
    path('profile' , views.profile , name = 'profile'),
]