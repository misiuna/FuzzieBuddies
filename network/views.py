from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
import json
from django.core.paginator import Paginator

from .models import *

import datetime
import fontawesome as fa

class NewPostForm(forms.Form):
    newPost = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': "What's on your mind?", 'style': 'width:100%; border-radius: 8px; border: 1px solid gray; padding: 8px;'}))

class EditPageForm(forms.Form):
    profileImg = forms.URLField(max_length=1050, label="Profile image:", widget=forms.TextInput(attrs={"placeholder" : "URL for your profile image", "style" : "width:100%; border-radius: 8px; border: 1px solid gray; padding: 8px; margin-bottom: 10px;"}))
    bannerImg = forms.URLField(max_length=1050, label="Cover photo:", widget=forms.TextInput(attrs={"placeholder" : "URL for your cover image", "style" : "width:100%; border-radius: 8px; border: 1px solid gray; padding: 8px; margin-bottom: 10px;"}))

# INDEX VIEW
def index(request):
    user = request.user #logged in user
    likedByUser = dict()
    allPosts = Post.objects.all().order_by('-timestamp')
    allLikes = Like.objects.all()

    for post in allPosts:
        userLikesThisPost = False
        for like in post.like_set.all():
            if like.user.username == user.username:
                userLikesThisPost = True
        likedByUser[post.id] = userLikesThisPost
        post.likedByUser = userLikesThisPost
        
    paginator = Paginator(allPosts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    userLikePosts = Like.objects.filter(user = user.id)
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            postCopy = form.cleaned_data["newPost"]
            timestamp = datetime.datetime.now()
            newPost = Post(user = user, post = postCopy, timestamp=timestamp)
            newPost.save()

            return HttpResponseRedirect(reverse( "index" ), {
                "form" : NewPostForm(),
                "allPosts" : Post.objects.all().order_by('-timestamp'),
                "page_obj" : page_obj,
                "allLikes" : allLikes,
                "userLikePosts" : userLikePosts,
                "user" : user,
                "likedByUser" : likedByUser
            })
    return render(request, "network/index.html", {
        "form" : NewPostForm(),
        "allPosts" : allPosts,
        "user" : user,
        "page_obj" : page_obj,
        "num_pages" : paginator.num_pages,
        "allLikes" : Like.objects.all(),
        "userLikePosts" : userLikePosts,
        "likedByUser" : likedByUser
    })

# USER PROFILE VIEW
@login_required(login_url="network:login")
def userProfile(request, username):
    profile = User.objects.get(username = username)
    
    #logged in user info
    user = request.user
    alreadyFollowing = Following.objects.filter(follower = user.id, followingOthers = profile.id)
    userFollowing = Following.objects.filter(follower = user)
    
    #profile user info
    profilePosts = Post.objects.filter(user = User.objects.get(username = username)).order_by("-timestamp")
    for post in profilePosts:
        userLikesThisPost = False
        for like in post.like_set.all():
            if like.user.username == user.username:
                userLikesThisPost = True
        post.likedByUser = userLikesThisPost

    paginator = Paginator(profilePosts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    profileFollowers = Following.objects.filter(followingOthers = User.objects.get(username = username).id)
    profileFollowing = Following.objects.filter(follower = User.objects.get(username = username))
        
    if request.method == "GET":
        alreadyFollowing.delete()
        return render(request,  "network/userProfile.html", {
            "profile" : User.objects.get(username = username),
            "profileFollowers" : profileFollowers,
            "profileFollowing" : profileFollowing,
            "profilePosts" : profilePosts,
            "alreadyFollowing" : alreadyFollowing,
            "page_obj" : page_obj,
            "num_pages" : paginator.num_pages,
            "user": user,
            "userFollowing" : userFollowing,        
        })

    if request.method == "POST":
        newFollowing = Following(follower = user, followingOthers = User.objects.get(username = username))
        newFollowing.save()    
        return render(request,  "network/userProfile.html", {
            "profile" : User.objects.get(username = username),
            "profileFollowers" : profileFollowers,
            "profileFollowing" : profileFollowing,
            "profilePosts" : profilePosts,
            "alreadyFollowing" : alreadyFollowing,
            "page_obj" : page_obj,
            "num_pages" : paginator.num_pages,
            "user": user,
            "userFollowing" : userFollowing,        
        })
    return render(request,  "network/userProfile.html", {
        "profile" : User.objects.get(username = username),
        "profileFollowers" : profileFollowers,
        "profileFollowing" : profileFollowing,
        "profilePosts" : profilePosts,
        "alreadyFollowing" : alreadyFollowing,
        "user": user,
        "userFollowing" : userFollowing,
        "page_obj" : page_obj,
        "num_pages" : paginator.num_pages,
    })

# EDIT PROFILE VIEW
@login_required(login_url="network:login")
def editProfile(request, username):
    profile = User.objects.get(username = username)
    profileFollowers = Following.objects.filter(followingOthers = User.objects.get(username = username).id)
    profileFollowing = Following.objects.filter(follower = User.objects.get(username = username))
    profilePosts = Post.objects.filter(user = User.objects.get(username = username)).order_by("-timestamp")
    user = request.user
    alreadyFollowing = Following.objects.filter(follower = user.id, followingOthers = profile.id)
    userFollowing = Following.objects.filter(follower = user)
    paginator = Paginator(profilePosts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.method == "POST":
        form = EditPageForm(request.POST)
        print(form.errors)
        if form.is_valid():
            profileImg = form.cleaned_data["profileImg"]
            coverImg = form.cleaned_data["bannerImg"]

            profile.profileImg = profileImg
            profile.coverImg = coverImg 
            profile.save()

            return render(request, 'network/userProfile.html', {
                "profile" : profile,
                "profileFollowers" : profileFollowers,
                "profileFollowing" : profileFollowing,
                "profilePosts" : profilePosts,
                "alreadyFollowing" : alreadyFollowing,
                "user": user,
                "userFollowing" : userFollowing,
                "page_obj" : page_obj,
                "num_pages" : paginator.num_pages,
            })
    return render(request, 'network/editProfile.html', {
        "form" : EditPageForm()
    })

# EDIT POST VIEW
@login_required(login_url="network:login")
def editPost(request, id):
    post = Post.objects.get(pk=id);
    if request.method == "PUT":
        update = json.loads(request.body)
        updatedPost = update.get("postText")

        post.post = updatedPost
        post.save()
        return HttpResponseRedirect(reverse( "index" ), {
            "form" : NewPostForm(),
            "allPosts" : Post.objects.all()
        })
    return HttpResponseRedirect(reverse( "index" ), {
            "form" : NewPostForm(),
            "allPosts" : Post.objects.all()
    })

# LIKE VIEW
@login_required(login_url="network:login")
def likePost(request, id):
    user= request.user
    post = Post.objects.get(pk=id)
    postAlreadyLiked = Like.objects.filter(user=user.id, post=post.id).count()
    #request.session['postAlreadyLiked'] = postAlreadyLiked

    if request.method == "POST":
        like = json.loads(request.body)
        newLike = like.get("id")
        

        newLikePost = Post.objects.get(pk=newLike)
        newLikeObject = Like(user=user, post = newLikePost)
        newLikeObject.save()
        return HttpResponseRedirect(reverse( "index" ), {
            "form" : NewPostForm(),
            "allPosts" : Post.objects.all().order_by('-timestamp'), 
            "postAlreadyLiked": postAlreadyLiked,
        }) 
    if request.method == "PUT":
        unlike = json.loads(request.body)
        newUnlike = unlike.get("id")

        newUnlikePost = Post.objects.get(pk=newUnlike)
        newUnlikeObject = Like.objects.get(user=user.id, post=newUnlikePost)
        newUnlikeObject.delete()
        postAlreadyLiked = Like.objects.filter(user=user.id, post=post.id).count()

        return HttpResponseRedirect(reverse( "index" ), {
            "form" : NewPostForm(),
            "allPosts" : Post.objects.all(), 
            "postAlreadyLiked": postAlreadyLiked,
            "isBreak" : False
        })

# FOLLOWING VIEW    
@login_required(login_url="network:login")
def following(request, username):
    user = request.user
    allPosts = Post.objects.all()
    followingNames = []
    for i in range(len(user.userFollowers.all())):
        name = user.userFollowers.all()[i].followingOthers.id
        followingNames.append(name)
       
    followingPosts = []
    for i in range(len(allPosts)):
        for j in range(len(followingNames)):
            if Post.objects.all()[i].user.id == followingNames[j]:
                post = Post.objects.all()[i]
                followingPosts.append(post)

    for post in followingPosts:
        userLikesThisPost = False
        for like in post.like_set.all():
            if like.user.username == user.username:
                userLikesThisPost = True
        post.likedByUser =  userLikesThisPost       

    paginator = Paginator(followingPosts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "followingPosts" : followingPosts,
        "page_obj" : page_obj,
        "num_pages" : paginator.num_pages,
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
