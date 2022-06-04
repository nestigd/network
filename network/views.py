import json
from hashlib import new
from http import HTTPStatus
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseNotFound, JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Following, User, Post
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import F, Case, When, Value



import logging

logger = logging.getLogger('django')
PAGINATION_AMOUNT = 4


# this is the main view of the website. 
# It displays "all" posts or posts by "followed" user. 
# This parameter needs to be provided in the url 
def index(request,  filter='all', page = 1):
    
    #protect against unexpected requests
    if filter not in ["all", "followed"]:
        filter = "all"

    if request.method == 'GET':
        return render(request, "network/index.html", {
            'filter' : filter,
            'page' : page})



    # this page also handles post submissions.
    if request.method == 'POST':
              
        # check authentication server-side.
        if not request.user.is_authenticated:
            return render(request, "network/index.html", {
                    'context' : "Sorry! You are not logged in. Log in to add a new post!",
                    'color' : "red",
                    "filter" : filter,
                    "page" : page,
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
                'page' : page
            })
            
            return render(request, "network/index.html", {
                'context' : 'Post shared!',
                'color' : "green",
                'filter' : filter,
                'page' : page
            })

        # exception handler for unforseen events
        except:
            return HttpResponse("unexpected exception occured, please inform an admin")


# Renders the User profile page
def user (request, id, page = 1):
    
    # get the user's data
    try:    
        profile_user =  User.objects.get(pk=id)
    
    # if not successfull redirect to "homepage"
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    
    currently_following = False 

    if request.user.is_authenticated:
        if request.user.following.filter(followed = profile_user).count() > 0:
            currently_following = True
    
    return render(request, "network/user.html", {
        #profile user will be used as filter (numeric) to fetch the relevant posts
        "profile_user" : profile_user,
        "currently_following" : currently_following,
        "page" : page,
    })


# Responds to AJAX request -> Sends post back as JSON data
# You must filter by: all, followed, userid # AND provide a page #
def posts (request, filter, page):

    # CASE #1: this will get all the posts in the database
    if filter == 'all':              
        posts = Post.objects.all()
    
    #CASE #2: only get the posts by followed users
    elif filter == 'followed':

        # handle case of Anonymous user by responding with error
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "error", 
                "alert_msg" : "Anonymous user isn't following any user"
            },  status=400)

        # filter the posts
        following = request.user.following.values_list("followed" , flat = True)
        posts = Post.objects.filter(poster__in = following)

    # CASE #3: only get posts by one specific user.
    elif filter.isnumeric():
        posts = Post.objects.filter(poster = int(filter))

    # CASE #4: wrong filter provided
    else:
        return JsonResponse({
            "status": "error", 
            "alert_msg" : "filter parameter is not valid"
        }, status=400)
    
    
    # create paginator with reverse chronological order. Then get the requested page from the paginator.
    posts_paginator = Paginator(posts.order_by("-timestamp").all(), PAGINATION_AMOUNT)
    post_page = posts_paginator.get_page(page)
    
    #prepare INFO + POST DATA for transmission
    serialized_page = [post.serialize() for post in post_page]
    info = {
            "post_count" : str(posts_paginator.count),
            "pages" : posts_paginator.num_pages,
            "has_previous" : post_page.has_previous(),
            "has_next" : post_page.has_next(),
            "this_page" : post_page.number,
        }
    
    # send data
    return JsonResponse({"info" : info, "page" : serialized_page}, safe=False)


# this view only accepts POST requests. 
# its only purpose is to overwrite old posts with new content
@login_required
def edit (request, post_id):

    print("request arrived")
    # check correct request method
    if not request.method == "POST":    
        error = f"received {request.method} request. Type must be: POST"
        logger.error(error)
        return HttpResponse(error)
    
    # get the requested post.  
    p = Post.objects.get(pk = post_id)
    print("p element created")
        
    # raise Exception if post not found. 
    # The post ID came from a fetch request from Javascript to the post() function, so there is no reason why the post now doesn't exist. 
    if not p:
        error = f"post with ID: {post_id} doesn't exist"
        logger.error(error)
        raise  Exception(error)
    
    # swap old content with the new
    p.body = request.POST.get("text")
    
    # Run tests
    try:
        assert p.is_valid_post()
        assert p.poster == request.user
        p.save()
        print("p saved")
    
    # respond with error if tests fail    
    except Exception as e:
        logger.error(e)
        return HttpResponse (e)
    
    print("going to redirect")
    return HttpResponseRedirect(reverse('user' , kwargs={"id" : request.user.id}))
    

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
        
        return JsonResponse({
            "status" : "OK",
            "alert_msg" : f"{followed_user.username} has now {followed_user.followers.count()} follower(s)"
            }, status=201)
    
    
# This is a catch-all function that redirects to the main index page with "all" as argument.
# It is useful to process bad requests without necessarily throwing a 404. 
def index_redirect (request):
    return HttpResponseRedirect(reverse("index"))






# ---------- EVERYTHING BELOW THIS LINE IS DITRIBUTION CODE. ALL CREDIT GOES TO THE CS_50 TEAM ---------------- #

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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

# THIS IS DITRIBUTION CODE 
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

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
