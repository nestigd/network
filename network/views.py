import json
from hashlib import new
from http import HTTPStatus
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import User, Post
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger('django')

# this is the main page of the website. It can be visited even if the user is not logged in.
# the view takes an argument that can be "all" or "following"...
# that will be passed down as context to the HTML and will be referenced by JS to fetch the correect posts.
def index(request, page):
    logger.info(f"got {request.method} request")
    logger.info(f"page filter{page}")

    # this returns the main page of the website
    if request.method == 'GET':
        return render(request, "network/index.html", {
            'page' : page
        })

    # POST HANDLING
    # ubmission of a new post.
    if request.method == 'POST':
        
        # check authentication server-side.
        if not request.user.is_authenticated:
            return render(request, "network/index.html", {
                    'context' : "Sorry! You are not logged in. Log in to add a new post!",
                    'color' : "red"
                })
            
        # if error checking ok, then create the new post.
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
                'color' : "green",
                'page' : 'all',
            })

        # exception handler, just in case
        except:
            return HttpResponse("unexpected exception occured, please inform an admin")


# This view displays all information and posts from a single user.
# from this page the user in question can be followed or unfollowed by the logged in user.
def user (request, id):
    profile_user =  User.objects.get(pk=id)
    return render(request, "network/user.html", {
        "profile_user" : profile_user,
    })


# This is a catch-all function that redirects to the main index page with "all" as argument.
# It is useful to process requests without arguments or to work around buggy url handling. 
def index_redirect (request):
    return HttpResponseRedirect(reverse("index", kwargs={'page': "all"}))

def login_view(request):
    logger.info(f"got {request.method} request")

    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index_redirect"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index_redirect"))


def register(request):
    
    logger.info(f"got {request.method} request")

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
        return HttpResponseRedirect(reverse("index_redirect"))
    else:
        return render(request, "network/register.html")


# this API will send post objects as JSON.abs
# filters needed:
# 'filter' : all, followed, user

def posts (request, filter):

    logger.info(f"got {request.method} request")

    # this will get all the posts in the database
    if filter == 'all':              
        logger.info("requested all posts")
        posts = Post.objects.all()
    
    # TODO: GET POSTS OF ALL FOLLOWED USERS
    elif filter == 'following':
        logger.info("requested following")

    # TODO: GET POSTS OF A SPECIFIC USER
    elif filter.isnumeric():
        logger.info("requested specific user's posts")
        posts = Post.objects.filter (poster = int(filter))

    else:
        return JsonResponse({"error: Bad request. invalid filter"}, status=400)
    
    
    posts = posts.order_by("timestamp").all()

    return JsonResponse([post.serialize() for post in posts], safe=False)

@csrf_exempt
def follow (request):

    data = json.loads(request.body)
    logger.info(f"request data is {data}")
    logger.info(f"got {request.method} request")
    logger.info(f"{request.user.username} wants to follow ....")
    #TODO:
    #elaborate JSON data form frontend
    # get following user username or ID
    # get followed user UN or ID
    
    # get the users from the database filtering with this data
    # make new Following object
    # test
    # save()
    
    return JsonResponse({"status : OK"}, status=400)