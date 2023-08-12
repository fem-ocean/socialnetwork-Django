
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("userprofile/<int:usernameid>", views.userprofile, name="userprofile"),
    path("following/<int:userid>", views.following, name="following"),


    # API Routes
    path("followbutton/<int:userid>", views.followButton, name="followbutton"),
    path("editpost/<int:postid>", views.editpost, name="editpost"),
    path("unlike/<int:postid>", views.unlike, name="unlike"),
    path("like/<int:postid>", views.like, name="like"),
    path("isliked/<int:postid>", views.isliked, name="isliked"),

]
