import json
from hashlib import new
from http import HTTPStatus
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Following, User, Post
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import logging
logger = logging.getLogger('django')

# this is the main page of the website. The view takes an argument that can be "all" or "following"... 
# The filter will determine which posts the user will see. JS will use this filter fetch the data from an API later defined in this file.

# This index view will also be responsible for handling POST requests containing new content from the users
def index(request, page):
    
    # CASE #1:
    # this returns the main page of the website
    if request.method == 'GET':
        return render(request, "network/index.html", {
            'page' : page
        })

    
    # CASE #2: POST
    # ubmission of a new post.
    if request.method == 'POST':
              
        # check authentication server-side.
        if not request.user.is_authenticated:
            return render(request, "network/index.html", {
                    'context' : "Sorry! You are not logged in. Log in to add a new post!",
                    'color' : "red"
                })
              
        # Create the new post.
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


# This is a catch-all function that redirects to the main index page with "all" as argument.
# It is useful to process bad requests without necessarily throwing a 404. 
def index_redirect (request):
    return HttpResponseRedirect(reverse("index", kwargs={'page': "all"}))


# This view displays all information and posts from a single user.
# from this page the user in question can be followed or unfollowed by the logged in user.
def user (request, id):
    try:    
        profile_user =  User.objects.get(pk=id)
    except ObjectDoesNotExist:
        arg = "all"
        return HttpResponseRedirect(reverse("index", kwargs = {"page" : arg}))
    
    return render(request, "network/user.html", {
        "profile_user" : profile_user,
    })


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




# this API will send post objects as JSON data
# an argument needs to be provided. You can filter by: all, followed, user

def posts (request, filter):

    logger.info(f"got {request.method} request")

    # CASE #1: this will get all the posts in the database
    if filter == 'all':              
        logger.info("requested all posts")
        posts = Post.objects.all()
    
    # TODO: CASE #2: This will only get the posts of followed users.
    # Follow() needs to be implemented before completing this.
    elif filter == 'following':
        logger.info("requested following")

    # CASE #3: Filter by a specific user ID.
    elif filter.isnumeric():
        logger.info("requested specific user's posts")
        posts = Post.objects.filter (poster = int(filter))

    else:
        return JsonResponse({"error: Bad request. invalid filter"}, status=400)
    
    # AFTER CASE 1,2, or 3 have taken place, order the query list. 
    posts = posts.order_by("timestamp").all()

    return JsonResponse([post.serialize() for post in posts], safe=False)




#TODO:
# OK - get following user username or ID
# get followed user UN or ID

# get the users from the database filtering with this data
# make new Following object
# test
# save()

@csrf_exempt
@login_required
def follow (request):
  
    # Check once again if the user is logged in. The decorator above already does this...
    # so this is redundant. I'll think about taking this out.
    if not request.user.is_authenticated:
        logger.info(f"got {request.method} request and user is authenticated")
        return JsonResponse({"status" : "user is not authenticated"}, status = 400)
    logger.info(f"got {request.method} request and user is authenticated")
       
    # this reads the data in the request body. Otherwise you only get to see "OBJECT object"
    try:
        data = json.loads(request.body)
    except:
        print("couldn't do json.loads() on received data")
    
    user_to_follow = User.objects.get(id = data.get('userToFollow'))
    user_who_follows = User.objects.get(id = request.user.id)
    
    # this is some basic error checking + JSON responses that will alert the user while exiting prematurely.
    if not user_who_follows or not user_to_follow:
        return JsonResponse({"status" : "one person has gone missing. Call 911 now!"}, status=400)
    
    if user_to_follow == user_who_follows:
        return JsonResponse({"status" : "can't follow yourself"}, status=400)
    
    # if no errors are found, we go ahead and save the new object.
    print(f"now will save {user_to_follow.username} and {user_who_follows.username}")
    new_following = Following(follower = user_who_follows, followed = user_to_follow)
    new_following.save()
    
    
    
    return JsonResponse({"status" : "OK",
                         "count" : f"{user_to_follow.username} has now {user_to_follow.followers.count()} follower(s)"}, status=201)