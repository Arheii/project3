
from django.urls import path

from . import views

app_name = "tweets"
urlpatterns = [
    path("", views.index, name="index"),
    path("user/<str:user_id>", views.user_page, name="user"),
    path("user/<str:user_id>/following", views.following_page, name="following"),
    path("user/<str:user_id>/follow", views.follow_or_unfollow, name="follow_or_unfollow"),
    path("tweet/<str:tweet_id>", views.like_or_dislike, name="like_or_dislike"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
