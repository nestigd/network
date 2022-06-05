
from django.urls import path

from . import views

urlpatterns = [
    # utility views: LOGIN, LOGOUT, REGISTER
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    #API routes
    path("posts/<slug:filter>&<int:page>", views.posts, name="posts"),
    path("follow", views.follow, name="follow"),
    path("like", views.like, name='like'),
    
    #This view handles POST forms, but it should really become an API route that handles AJAX requests at some point.
    #Users should not have to reload an entire page just to edit a post.
    path("edit/<int:post_id>", views.edit, name="edit"),
    
    # main views: INDEX, USER
    path("user/<int:id>", views.user, name="user"),
    path("user/<int:id>/page<int:page>", views.user, name="user"),
    path("", views.index, name="index"),
    path("<str:filter>", views.index, name="index"),
    path("<str:filter>/page<int:page>", views.index, name="index"),
    
    
]                                                                                                                                                                                   
