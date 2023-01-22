from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register),
    path('login/', login_view),
    path('logout/', logout),
    path('follow/', give_follow),
    path('give/like/', give_like),
    path('unfollow/', unfollow),
    path('leave/comment/', leave_comment),
    path('get/liked/', get_liked),
    path('<str:pk>/', get_user_username),
    path('create/post/', create_post),
    path('get/post/<int:pk>/', get_post),
    path('follow/post/', get_post_follow),
    path('create/stories/', create_stories),
    path('delete/post/<int:pk>/', delete_post),
    path('delete/stories/<int:pk>/', delete_stories),
    path('delete/comment/<int:pk>/', delete_comment),
]
