from hashlib import new
from http import HTTPStatus
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import User, Post
import logging
logger = logging.getLogger('django')

# this is the main page of the website. It can be visited even if the user is not logged in.
# the view takes an argument that will be passed down as context to the HTML and will be referenced by JS to fetch the correect posts.
def index(request, page):
    logger.info(page)
    print("got request")
    # this returns the main page of the website
    if request.method == 'GET':
        return render(request, "network/index.html", {
            'page' : page
        })

    # this handles the submission of a new post.
    if request.method == 'POST':
        
        # check authentication server-side too.
        if not request.user.is_authenticated:
            return render(request, "network/index.html", {
                    'context' : "Sorry! You are not logged in. Log in to add a new post!",
                    'color' : "red"
                })
            
        # if all is ok, then create the new post.
        try:
            user = request.user
            post_text = request.POST.get("text")
            p = Post(poster=user,body = post_text)

            # just some console logs to facilitate testing.
            logger.info(f"user: {user} body {post_text}")
            logger.info (p.is_valid_post())
            logger.info(f"object {p}")

            # run tests on new posts before saving
            if not p.is_valid_post():
                
                # test failed: inform user that the post wasn't succesfully saved
                return render(request, "network/index.html", {
                    'context' : "Sorry! Your post wasn't saved because an exception has occurred. Please inform an admin",
                    'color' : "red"
                })

            # test passed: save the data and render the index page informing the user that the post was saved.
            p.save()
            return render(request, "network/index.html", {
                'context' : 'Post shared!',
                'color' : "green"
            })

        # exception handler, just in case
        except:
            return HttpResponse("unexpected exception occured, please inform an admin")
        
def index_redirect (request):
    return HttpResponseRedirect(reverse("index", kwargs={'page': "all"}))

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
# filters needed:
# 'filter' : all, followed, user

def posts (request, filter):

    # this will get all the posts in the database
    if filter == 'all':              
        logger.info("requested all posts")
        posts = Post.objects.all()
        
    # TODO: GET POSTS OF ALL FOLLOWED USERS

    # TODO: GET POSTS OF A SPECIFIC USER

    posts = posts.order_by("timestamp").all()

    return JsonResponse([post.serialize() for post in posts], safe=False)