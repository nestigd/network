
from django.urls import path

from . import views

urlpatterns = [
    path("home/<str:page>", views.index, name="index"),
    path("", views.index_redirect, name="index_redirect"),                                  
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),


    #API routes
    path("posts/<slug:filter>", views.posts, name="posts"),

]                                                                                                                                                                                   
