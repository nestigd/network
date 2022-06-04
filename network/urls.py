
from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    # paths to main view
    path("user/<int:id>", views.user, name="user"),
    path("user/<int:id>/page<int:page>", views.user, name="user"),
    path("", views.index, name="index"),
    path("<str:filter>", views.index, name="index"),
    path("<str:filter>/page<int:page>", views.index, name="index"),
    
    path("edit/<int:post_id>", views.edit, name="edit"),

    
    #API routes
    path("posts/<slug:filter>&<int:page>", views.posts, name="posts"),
    path("follow", views.follow, name="follow"),

]                                                                                                                                                                                   
