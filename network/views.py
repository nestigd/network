import logging
logger = logging.getLogger('django')


from hashlib import new
from http import HTTPStatus
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post


def index(request):

    # this returns the main page of the website
    if request.method == 'GET':
        return render(request, "network/index.html")



    # this handles the submission of a new post by a registered user.
    if request.method == 'POST' and request.user.is_authenticated:

        try:
            # create the new post
            user = request.user
            post_text = request.POST.get("text")
            p = Post(poster=user,body = post_text)

            # just some console logs to help with debugging... self explainatory, I know...
            logger.debug(f"user: {user} body {post_text}")
            logger.debug (p.is_valid_post())
            logger.debug(f"object {p}")

            # run tests on new posts before saving
            if not p.is_valid_post():
                
                # inform user that the post wasn't succesfully saved
                return render(request, "network/index.html", {
                    'context' : "Sorry! Your post wasn't saved because an exception has occurred. Please inform an admin",
                    'color' : "red"
                })

            # if all tests pass, save the data and render the index page informing the user that the post was saved.
            p.save()
            return render(request, "network/index.html", {
                'context' : 'Post shared!',
                'color' : "green"
            })

        # exception handler, just in case
        except:
            return HttpResponse("unexpected exception occured, please inform an admin")

        





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


# this API will send post objects as JSON.abs
# parameters needed:kk
# 'filter' : all, followed, user

def posts (request, parameter):

    # TODO: GET ALL POSTS
    if parameter == 'all':
        
        logger.info("requested all posts")
        posts = Post.objects.all()        
        pass

    # TODO: GET POSTS OF ALL FOLLOWED USERS

    # TODO: GET POSTS OF A SPECIFIC USER

    posts = posts.order_by

    pass