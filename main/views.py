from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from main.models import account_info, posts, messaging, saved_posts
from main.forms import new_posts
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import date
import json

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Incorrect details")

    return render(request, "login.html")

def confirm_delete_page(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            if any (User.objects.filter(username=request.user,password=request.POST['password2'])):
                User.objects.get(username=request.user,password=password2).delete()
            else:
                messages.info(request, "Incorrect password")
        else:
            messages.info(request, "Passwords do not match")

    return render(request, "confirm_delete.html")

def user_info_page(request):
    context = {'user':account_info.objects.get(user=User.objects.get(username=request.user))}
    return render(request, "user_info.html", context)

def new_posts_page(request):
    context = {'posts':posts.objects.all()}
    if request.method == "POST":
        posts(user=request.user,caption=request.POST['caption'],
                file_uploaded=request.FILES['file_uploaded'], date = date.today()).save()
    return render(request, "new_post.html",context)

def comments_page(request):
    return render(request, "comments.html")

def follow_page(request):
    return render(request, "follow.html")

def group_media_page(request):
    return render(request, "group_media.html")

def activities_page(request):
    return render(request, "activities.html")

def ask_delete_page(request):
    return render(request, "ask_delete.html")

def saved_posts_page(request):
    context = {'saved_posts':saved_posts.objects.filter(user=request.user)}
    return render(request, "saved.html",context)

def notifications_page(request):
    return render(request, "notifications.html")

def settings_page(request):
    return render(request,"settings_page.html")

def email_verification_page(request):
    return render(request, "email_verification.html")

def join_meetings_page(request):
    return render(request, "join_meeting.html")

def loading_page(request):
    return render(request,"loading.html")

def accept_page(request):
    return render(request, "accept.html")

def meetings_page(request):
    return render(request, "meetings.html")

def sign_up_page(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == "POST" and "vschools_first_name" in request.POST:
        request.session["vschools_first_name"] = request.POST['first_name']
        request.session["vschools_last_name"] = request.POST['last_name']
        request.session["vschools_email"] = request.POST['email']

        return redirect('new_password')
    return render(request,"sign_up.html")

def new_password_page(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            request.session["password"] = request.POST["password2"]
            username = request.session['vschools_first_name'] + " " + request.session["vschools_last_name"]
            new_user=User.objects.create_user(username=username,email=request.session['vschools_email'],
                                        password=request.POST['password2'])

            account_info(user=new_user,datejoined=date.today()).save()

            user = authenticate(username=username,password=request.POST["password2"])

            if user is not None:
                login(request, user)
                del request.session["vschools_first_name"]
                del request.session["vschools_last_name"]
                del request.session["vschools_email"]
                return redirect("get_started")
    return render(request,"new_password.html")

def messages_page(request):
    context = {'messaging':messaging.objects.filter(sender_id=request.user.id,receiver_id=request.user.id)}

    return render(request, "messages.html", context)

def advertisements_page(request):
    return render(request, "advertisements.html")

def groups_page(request):
    return render(request, "groups.html")

def person_info_page(request):
    return render(request,"person.html")

def live_page(request):
    return render(request, "live.html")

def guest_page(request):
    return render(request, "guest.html")

@login_required(login_url='login')
def home_page(request):
    user = account_info.objects.get(user=request.user)
    context = {'posts':posts.objects.all(),'user':user, 
                'saved_posts':saved_posts.objects.filter(user=request.user)}
    if request.is_ajax:
        if request.body:
            if 'save' in json.loads(request.body):
                saved_posts(user=request.user,
                    post=posts.objects.get(id=json.loads(request.body)['save'])).save()
            elif 'like' in json.loads(request.body):
                print('like')
        

    return render(request, "home.html",context)

def get_started_page(request):
    return render(request, "get_started.html")

def logout_user(request):
    logout(request)
    return redirect('login')

def test_page(request):
    return render(request, "test.html")
