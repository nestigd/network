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
from django.core.paginator import Paginator


import logging

logger = logging.getLogger('django')


# this is the main view of the website. 
# It displays "all" posts or posts by "followed" user. 
# This parameter needs to be provided in the url 
def index(request,  filter):
    
    if request.method == 'GET':
        return render(request, "network/index.html", {
            'filter' : filter
        })



    # this page also handles post submissions.
    if request.method == 'POST':
              
        # check authentication server-side.
        if not request.user.is_authenticated:
            return render(request, "network/index.html", {
                    'context' : "Sorry! You are not logged in. Log in to add a new post!",
                    'color' : "red",
                    "filter" : filter
                })
              
        # generate the new post object.
        try:
            user = request.user
            post_text = request.POST.get("text")
            p = Post(poster=user,body = post_text)

            # TODO: implement better testing
            try:
                assert p.is_valid_post()
                # save posts if tests pass
                p.save()
                
            except:
                return render(request, "network/index.html", {
                'context' : 'not shared! there was a problem and it could not be saved to the server',
                'color' : "red",
                'filter' : filter,
            })
            
            return render(request, "network/index.html", {
                'context' : 'Post shared!',
                'color' : "green",
                'filter' : filter,
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
        return HttpResponseRedirect(reverse("index", kwargs = {"filter" : "all"}))
    
    currently_following = False 

    if request.user.is_authenticated:
        if request.user.following.filter(followed = profile_user).count() > 0:
            currently_following = True
    
    return render(request, "network/user.html", {
        "profile_user" : profile_user,
        "currently_following" : currently_following,
    })

# this API will send post objects as JSON data
# an argument needs to be provided. You can filter by: all, followed, user

def posts (request, filter):

    # handle anonymous user before it become a problem
    if not request.user.is_authenticated:
        filter = 'all'
    
    # CASE #1: this will get all the posts in the database
    if filter == 'all':              
        posts = Post.objects.all()
    
    #CASE #2: only get the posts by followed users
    elif filter == 'followed':
      
        following = request.user.following.values_list("followed" , flat = True)
        posts = Post.objects.filter(poster__in = following)

    # CASE #3: only get posts by one specific user.
    elif filter.isnumeric():
        posts = Post.objects.filter (poster = int(filter))

    else:
        message.append("invalid filter")
        return JsonResponse({
            "status": "error", 
            "alert_msg" : message
        }, status=400)
    
    # reverse chronological order. 
    posts = Paginator(posts.order_by("-timestamp").all(), 5)
    post_page = posts.get_page(1)

    return JsonResponse([post.serialize() for post in post_page], safe=False)


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
    return HttpResponseRedirect(reverse("index", kwargs={'filter': "all"}))






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
