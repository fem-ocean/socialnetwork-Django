from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse 
from django.db.models import Count, Case, When, BooleanField, Q, OuterRef, Subquery, Exists
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


from .models import User, Post, Like, Follower


def index(request):

    #All posts and number of likes
    allPosts = Post.objects.annotate(number_of_likes=Count('likedpost')).order_by('-id')


    # PAGINATOR Divides all the posts into pages. 10 per page
    paginator = Paginator(allPosts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    allLikes = Like.objects.all()
    allPostsLiked = []
    try:
        for like in allLikes:
            if like.user.id == request.user.id:
                allPostsLiked.append(like.post.id)
    except:
        allPostsLiked = []
    # print(allPostsLiked)

    # Create a new post
    if request.user.is_authenticated:
        if request.method == 'POST':
            content = request.POST["newpost"]
            
            #create and save the content to the Post table in database
            Post.objects.create(owner=request.user, content=content)
            # return HttpResponseRedirect(reverse("index"))
            return render(request, "network/index.html", {
                "allPosts": allPosts,
                "page_obj": page_obj,
            	"allPostsLiked": allPostsLiked       
            })
    
    return render(request, "network/index.html", {
        "allPosts": allPosts,
        "page_obj": page_obj,
        "allPostsLiked": allPostsLiked       
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
    user_to_follow = Follower.objects.filter(user=userProfileShow)
    user_to_follow_num = user_to_follow.count()

    # number following
    user_following = Follower.objects.filter(follower=userProfileShow)
    user_following_num = user_following.count()

    # post in reverse chronolological order of profile owner  
    ownerPosts = Post.objects.filter(owner=userProfileShow).annotate(number_of_likes=Count('likedpost')).order_by('-id')   

    # PAGINATION
    # Divides all your posts into pages. 10 per page
    paginator = Paginator(ownerPosts, 10)
    # get page from frontend
    page_number = request.GET.get('page')
    # page_obj requested for and to be rendered as context based on what user asked for.
    page_obj = paginator.get_page(page_number)

    if request.user ==userProfileShow:
        user_own_profile = True
    else:
        user_own_profile = False   

    return render(request, "network/userprofile.html", {
        "userDetails": userProfileShow,
        "user_to_follow_num": user_to_follow_num,
        "user_following_num": user_following_num,
        "ownerPosts": ownerPosts,
        "user_own_profile": user_own_profile,
        "page_obj": page_obj
    })



@csrf_exempt
def followButton(request,userid):

    # Get the user to follow or unfollow
    usertofollow = User.objects.get(pk=userid)

    #instance of the user to follow in Follow table
    person = Follower.objects.filter(user=usertofollow)

    #Get the current user
    current_user = get_object_or_404(User, pk=request.user.id)
    
    is_follower = person.filter(follower=request.user).exists()
    # print(is_follower)
    
    
    if request.method == "PUT":
        # Grab the value from the API on the frontend(True or False)
        data = json.loads(request.body)
        user_is_a_follower = data["userisafollower"]

        if user_is_a_follower:
            Follower.objects.create(user=usertofollow, follower=request.user)
            # print("added successfully")
        else:
            f = Follower.objects.get(user=usertofollow, follower=request.user)
            f.delete()
            # print(f"removed successfully")
        return JsonResponse({"userisafollower": is_follower},status=201)
    
    return JsonResponse({"userisafollower": is_follower}, status=201)



def following(request, userid):

    # Get all instances where the follower is the current user
    current_user_followings = Follower.objects.filter(follower=request.user)

    # Get the list of users from each instances
    list_of_users_following = [users.user for users in current_user_followings]

    # Query all posts from Post table the current user is following
    posts_user_is_following = Post.objects.filter(owner__in=list_of_users_following).annotate(number_of_likes=Count('likedpost')).order_by('-id')

    # print(posts_user_is_following)
        
    paginator = Paginator(posts_user_is_following, 4)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    
    return render(request, "network/following.html", {
        "page_obj": page_object
    })
           

@csrf_exempt
def editpost(request, postid):
    if request.method =="PUT":
        data = json.loads(request.body)
        editedContent = data["content"]

        post_to_be_edited = Post.objects.get(pk=postid)
        post_to_be_edited.content = editedContent
        post_to_be_edited.save()

        # print("successfully edited")

        return JsonResponse({"content": editedContent}, status=201)

@csrf_exempt
def unlike(request, postid):
    post_received = Post.objects.get(id=postid)
    unlikedpost = Like.objects.filter(user=request.user, post=post_received )
    # print(unlikedpost)
    
    unlikedpost.delete()
    

    return JsonResponse({'message':'unliked successfully'})
     


@csrf_exempt
def like(request, postid):
    post_to_like = Post.objects.get(id=postid)
    likedpost = Like(user=request.user, post=post_to_like)
    likedpost.save()

    updated_post_likes = Like.objects.filter(post=post_to_like).count()
    # print(f"number of post liked:{updated_post_likes}")

    return JsonResponse({'message': 'liked successfully',
                         'updated_post_likes': updated_post_likes
                         })

    

@csrf_exempt
def isliked(request,postid):

    # Get the user to follow or unfollow
    post_to_check = Post.objects.get(pk=postid)

    #Get the current user
    current_user = get_object_or_404(User, pk=request.user.id)

    #instance of the post to check if it exist in  in Like table
    like_instance = Like.objects.filter(post=post_to_check, user=current_user)

    
  
    if len(like_instance) >= 1:
        is_liked = True
    else:
        is_liked = False
   
 
    return JsonResponse({"is_liked": is_liked}, status=201)

