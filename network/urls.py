
from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("", views.index, name="index"),
    path("userProfile/<str:username>", views.userProfile, name="userProfile"),
    path("editProfile/<str:username>", views.editProfile, name="editProfile"),
    path("editPost/<int:id>", views.editPost, name="editPost"),
    path("following/<str:username>", views.following, name="following"),
    path("likePost/<int:id>", views.likePost, name="likePost")
    
]
