from hashlib import new
from http import HTTPStatus
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# New posts will be added through this view
def post (request):

    print(request.method)
    # Make sure that only post requests are processed.abs
    if request.method != 'POST':
        # Tell the user: result NG by showing a message at the top of the page
        return render(request, "network/index.html", {
            'context' : 'request method was not POST',
            'color' : "red"

        })

    # store the data from the request in variables.
    user = request.user
    post_text = request.POST.get("text")

    # create the post object and save it
    try:
        p = Post(poster=user,body = post_text)
        p.save()

        # ALL OK! Tell the user!
        return render(request, "network/index.html", {
            'context' : 'Post shared!',
            'color' : "green"
        })

    except:
        # something went wrong. Tell the user to call an admin
        return render(request, "network/index.html", {
            'context' : 'Sorry! An exception has occurred. Please inform an admin',
            'color' : "red"

        })
        
    
