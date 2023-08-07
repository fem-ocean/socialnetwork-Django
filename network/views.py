from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse 
from django.db.models import Count
import json
from django.views.decorators.csrf import csrf_exempt



from .models import User, Post, Like, Follower, Following


def index(request):

    #All posts and number of likes
    allPosts = Post.objects.annotate(number_of_likes=Count('likedpost__liked')).order_by('-id')


    # Create a new post
    if request.user.is_authenticated:
        if request.method == 'POST':
            content = request.POST["newpost"]
            
            #save the content to the Post table in database
            Post.objects.create(owner=request.user, content=content)
            # return HttpResponseRedirect(reverse("index"))
            return render(request, "network/index.html", {
                "allPosts": allPosts,
                # "numberOfLike": numberOfLike
            })
    
    return render(request, "network/index.html", {
        "allPosts": allPosts,
        # "numberOfLike": numberOfLike
    })

    


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
    



def userprofile(request, usernameid):
    
    # Get instance of the user clicked on from the User table
    userProfileShow = User.objects.get(pk=usernameid)

    # number of followers
    followersCount = sum(people.follower.count() for people in Follower.objects.filter(user= userProfileShow))

    # number following
    followingCount = sum(people.following.count() for people in Following.objects.filter(user=userProfileShow))

    # post in reverse chronolological order of profile owner  
    ownerPosts = Post.objects.filter(owner=userProfileShow).order_by('-id')   

    if request.user ==userProfileShow:
        user_own_profile = True
    else:
        user_own_profile = False   

    return render(request, "network/userprofile.html", {
        "userDetails": userProfileShow,
        "followersCount": followersCount,
        "followingCount": followingCount,
        "ownerPosts": ownerPosts,
        "user_own_profile": user_own_profile

    })



@csrf_exempt
def followButton(request,userid):

    # Get the user to follow or unfollow
    usertofollow = User.objects.get(pk=userid)
    # print(usertofollow) - for debugging

    #instance of the user to follow in Follow table
    person = Follower.objects.filter(user=usertofollow)

    #current user
    current_user = get_object_or_404(User, pk=request.user.id)

    
    is_follower = person.filter(follower=request.user).exists()
    print(is_follower)
    
    
    if request.method == "PUT":
        # Grab the value from the API on the frontend(True or False)
        data = json.loads(request.body)
        user_is_a_follower = data["userisafollower"]

        followerInstance, created = Follower.objects.get_or_create(user=usertofollow)

        if user_is_a_follower:
            followerInstance.follower.add(current_user)
            print("added successfully")
        else:
            followerInstance.follower.remove(current_user)
            print(f"removed successfully")
        return JsonResponse({"userisafollower": is_follower},status=201)
    
    
    
    return JsonResponse({"userisafollower": is_follower}, status=201)



def following(request, userid):

    #get posts from the all the profiles the current user is following

    # step1 - get the users who the current user is following from the following table
    #step2 -  filter all posts in the Post table by the users gotten from step 1
    

    
    return render(request, "network/following.html")
           
