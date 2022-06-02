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



# use "all" or "following" page parameter to decide which set of posts to view.
def index(request, page):
    
    # CASE #1:
    # this returns the main page of the website
    if request.method == 'GET':
        return render(request, "network/index.html", {
            'page' : page
        })

    # CASE #2: POST
    # Handles POST requests containing the new content created by the users
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

            # TODO: better tests need to be implemented
            assert p.is_valid_post()

            # tests passed: save the data and render the index page informing the user that the post was saved.
            p.save()
            
            return render(request, "network/index.html", {
                'context' : 'Post shared!',
                'color' : "green",
                'page' : 'all',
            })

        # exception handler for unforseen events
        except:
            return HttpResponse("unexpected exception occured, please inform an admin")


# User profile page
def user (request, id):
    
    # get the user's data
    try:    
        profile_user =  User.objects.get(pk=id)
    
    # if not successfull redirect to "homepage"
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse("index", kwargs = {"page" : "all"}))
    
    currently_following = False 
   
    if request.user.following.filter(followed = profile_user).count() > 0:
        currently_following = True
    
    return render(request, "network/user.html", {
        "profile_user" : profile_user,
        "currently_following" : currently_following,
    })

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
        return JsonResponse({
            "status": "error", 
            "alert_msg" : "invalid filter"
        }, status=400)
    
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


# creates or deletes Following objects
# returns a JSON response. 
# if the response contains "status" : OK, javascript will change the behavious of the follow/unfollow button in the front end
@csrf_exempt
@login_required
def follow (request):
  
    # Reads the data in the request body. 
    try:
        data = json.loads(request.body)
        operation = data.get("operation")
    except:
        print("couldn't do json.loads() on received data")
    
    followed_user = User.objects.get(id = data.get('userToFollow'))
    following_user = User.objects.get(id = request.user.id)
    
    # Basic error checking
    if not following_user or not followed_user:
        return JsonResponse({
            "status" : "error",
            "alert_msg" : "one person has gone missing. Call 911 now!"
            }, status=400)
    
    if followed_user == following_user:
        return JsonResponse({
            "status" : "error",
            "alert_msg" : "can't follow/unfollow yourself"
            }, status=400)
    
    alreadyfollows = (following_user.following.filter(followed = followed_user).count() > 0) == True
    
    # CASE #1 FOLLOW THE USER:
    if operation == "Follow":
        
        if  alreadyfollows:
            return JsonResponse({
                "status" : "bad request",
                "alert_msg" : f"you already follow {followed_user.username}",
                }, status=400)
        
        new_following = Following(follower = following_user, followed = followed_user)
        new_following.save()
        
        return JsonResponse({
            "status" : "OK",
            "alert_msg" : f"{followed_user.username} has now {followed_user.followers.count()} follower(s)"
            }, status=201)
    
    #CASE #2 UNFOLLOW THE USER:
    if operation == "Unfollow":
        
        if not alreadyfollows:
            return JsonResponse({"status" : "bad request",
                            "alert_msg" : f"you don't follow {followed_user.username} currently",
                            }, status=400)
            
        old_following = Following.objects.filter(follower = following_user, followed = followed_user).all()
        old_following.delete()
        print("succesfully deleted")
        
        return JsonResponse({
            "status" : "OK",
            "alert_msg" : f"{followed_user.username} has now {followed_user.followers.count()} follower(s)"
            }, status=201)
    
    
    
    
    
    
    
    
    
    
    
    
# This is a catch-all function that redirects to the main index page with "all" as argument.
# It is useful to process bad requests without necessarily throwing a 404. 
def index_redirect (request):
    return HttpResponseRedirect(reverse("index", kwargs={'page': "all"}))



# ---------- EVERYTHING BELOW THIS LINE IS DITRIBUTION CODE. ALL CREDIT GOES TO THE CS_50 TEAM ---------

# THIS IS DITRIBUTION CODE 
def login_view(request):

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

# THIS IS DITRIBUTION CODE 
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index_redirect"))

# THIS IS DITRIBUTION CODE 
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



