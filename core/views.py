import re
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from itertools import chain
import random

from .models import Followercount, Likepost, Profile, Post

# Create your views here.
@login_required(login_url = 'signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    #post feed code
    user_following_list = []
    feed = []

    user_following_objects = Followercount.objects.filter(follower=request.user.username)

    for objects in user_following_objects:
        user_following_list.append(objects.user)
    
    for username in user_following_list:
        feeds_of_username = Post.objects.filter(user=username)
        feed.append(feeds_of_username)
    feed_list = list(chain(*feed))

    #user suggestions code:
    all_users = []
    all_users = User.objects.all()
    all_users_ids = []
    
    for a_user_object in all_users:
        all_users_ids.append(a_user_object.id)
    
    all_users_ids.remove(request.user.id)

    for user_1 in user_following_list:
        remove_id_object = User.objects.get(username=user_1)
        remove_id = remove_id_object.id
        all_users_ids.remove(remove_id)

    suggestion_profile_list = []
    for s_user in all_users_ids:
        suggestion_profile_object = Profile.objects.filter(id_user=s_user)
        suggestion_profile_list.append(suggestion_profile_object)
    
    chained_suggestion_profile_list = list(chain(*suggestion_profile_list))

    return render(request, 'index.html', {'user_profile': user_profile, 'posts': feed_list, 'chained_suggestion_profile_list': chained_suggestion_profile_list})

@login_required(login_url = 'signin')
def search(request):
    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.filter(user=user_object)

    user_id_list = []
    user_profile_list = []

    username=request.POST['username']    

    user_object_list = User.objects.filter(username__icontains=username)

    for object in user_object_list:
        user_id_list.append(object.id)
    
    for id in user_id_list:
        user_profile_item = Profile.objects.filter(id_user=id)
        user_profile_list.append(user_profile_item)
    
    user_profile_list = list(chain(*user_profile_list))

    return render(request, 'search.html', {'user_profile': user_profile, 'user_profile_list': user_profile_list})

@login_required(login_url = 'signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_flag = Likepost.objects.filter(username=username, post_id=post_id).first()

    if like_flag == None:
        new_like = Likepost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes += 1
        post.save()
        return redirect('/')
    else:
        like_flag.delete()
        post.no_of_likes -= 1
        post.save()
        return redirect('/')

@login_required(login_url = 'signin')
def settings(request):
    user_profile = Profile.objects.get(user = request.user)

    if request.method == 'POST':
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
        else:
            image = user_profile.profileimg

        bio = request.POST['bio']
        location = request.POST['location']

        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()

        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})

def signup(request):
    
    if request.method == 'POST':
        var_username = request.POST['username']
        var_email = request.POST['email']
        var_password = request.POST['password']
        var_password2 = request.POST['password2']

        if var_password!=var_password2:
            messages.info(request, "Passwords Didn't Matched. Please Try Again")
            return redirect('signup')
        elif(User.objects.filter(email=var_email).exists()):
            messages.info(request, "An account with this Email address already exists.")
            return redirect('signup')
        elif(User.objects.filter(username=var_username).exists()):
            messages.info(request, "Account with that user already exists. Please use different username")
            return redirect('signup')
        else:
            user = User.objects.create_user(username=var_username, email=var_email, password=var_password)
            user.save()

            user_login = auth.authenticate(username=var_username, password=var_password)
            auth.login(request, user_login)

            user_model_object = User.objects.get(username=var_username)
            new_profile = Profile.objects.create(user=user_model_object, id_user=user_model_object.id)
            new_profile.save()
            
            return redirect('settings')

    else:
        return render(request, 'signup.html')

def signin(request):

    if request.method=='POST':
        var_username = request.POST['username']
        var_password = request.POST['password']

        user = auth.authenticate(username=var_username, password=var_password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Invalid Credentials")
            return render(request, 'signin.html')
    else:
        return render(request, 'signin.html')

@login_required(login_url = 'signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=user_object.username)
    no_of_user_posts = len(user_posts)

    follower = request.user.username
    user = pk

    user_follower_list = Followercount.objects.filter(user=pk)
    user_following_list = Followercount.objects.filter(follower=pk)

    user_followers = len(user_follower_list)
    user_following = len(user_following_list)

    if Followercount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    context = {
        'user_followers': user_followers,
        'user_following': user_following,
        'user_follower_list': user_follower_list,
        'user_following_list': user_following_list,
        'button_text': button_text,
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'no_of_user_posts': no_of_user_posts
    }
    return render(request, 'profile.html', context)

@login_required(login_url = 'signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        # print(new_post.caption)

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url = 'signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        follow_object = Followercount.objects.filter(follower=follower, user=user).first()

        if follow_object is None:
            new_follow_object = Followercount.objects.create(follower=follower, user=user)
            new_follow_object.save()
            return redirect('/profile/'+user)
        else:
            follow_object.delete()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url = 'signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')