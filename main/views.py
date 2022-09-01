from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import JsonResponse
from main.models import account_info, followings, Room, Room_member, Room_message
from datetime import date, timedelta, datetime
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from .utils import *
from django.core.mail import EmailMessage
import json
import random
import re
import secrets
import time
import uuid
from agora_token_builder import RtcTokenBuilder


def getToken(request):
    appId = '0eb3e08e01364927854ee79b9e513819'
    appCertificate = 'f2fdb8604d8b47a9bc71dcd5606f1d7e'
    channelName = request.GET.get('channel')
    uid = request.user.id
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token}, safe=False)

def join_session(request):
    data = request.GET
    passcode = data['passcode']
    if any(Room.objects.filter(passcode=passcode)):
        return JsonResponse({'meeting_id':Room.objects.get(passcode=passcode).room_name}, safe=False)
    else:
        return JsonResponse({'not_found':True}, safe=False)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, """Dear user your details are incorrect please check them and try again
                        or follow the forgot password link if you have forgoten your password.""")

    return render(request, "login.html")

def getRoomMembers(request):
    room_name = reqeust.GET.get('room_name')
    target = Room.objects.filter(room_name=room_name)
    response = []
    for item in target:
        dict_item = {'name':room.user.username}
        dict_item['profile_picture'] = account_info.objects.get(user=item.user).profile_picture.url
        dict_item['uid'] = item.uid

    return JsonResponse(response, safe=False)

def followUser(request):
    data = json.loads(request.body)
    user_id = data['user_id']
    user = User.objects.get(id=int(user_id))
    if request.user.id not in [item.follower.id for item in followings.objects.filter(user=user)]:
        followings(user=user,follower=request.user).save()

def unfollowUser(request):
    data = json.loads(request.body)
    user_id = data['user_id']
    user = User.objects.get(id=int(user_id))
    if request.user.id in [item.follower.id for item in followings.objects.filter(user=user)]:
        followings.objects.get(user=user,follower=request.user).delete()

def getRoomMember(request):
    uid = request.GET['uid']
    user = User.objects.get(id=int(uid))
    room_name = request.GET['room_name']
    user_token = account_info.objects.get(user=user).user_token
    print(account_info.objects.get(user=user).profile_picture.url)
    response = {'name':user.username,
               'profile_picture':account_info.objects.get(user=user).profile_picture.url,
              'user_token':user_token,'uid':user.id}
    print(response)
    return JsonResponse(response, safe=False)

@login_required(login_url='login')
def ask_delete_page(request):
    return render(request, "ask_delete.html")

@login_required(login_url='login')
def studio_page(request):
    return render(request,"studio.html")

@login_required(login_url='login')
def settings_page(request):
    user = request.user
    context = {'user':user}
    user.token = account_info.objects.get(user=user).user_token

    if account_info.objects.get(user=request.user).profile_picture:
        user.profile_picture = account_info.objects.get(user=request.user).profile_picture

    if request.method == "POST":
        if request.FILES:
            item = account_info.objects.get(user=request.user)
            item.profile_picture = request.FILES['image']
            item.save()
    
    return render(request,"settings_page.html",context)

def password_changed(request):
    return render(request,"password_changed.html")

def email_verification_page(request):
    return render(request, "email_verification.html")

def verify_email_page(request):
    return render(request, 'verify_email_page.html')

def verify_email(request, token):
    try:
        obj = account_info.objects.get(email_token=token)
        obj.email_verified = True
        obj.save()
        return redirect('get_started')
    except Exception as e:
        print('invalid token')    

def sign_up_page(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password_one = request.POST['password_one']
        password_two = request.POST['password_two']
        email = request.POST['email']
        username = first_name + " " + last_name

        if not any([email == item.email for item in User.objects.all()]):
            if password_one == password_two:
                user = User.objects.create_user(username,email,password_two)
                user.first_name = first_name
                user.last_name = last_name
                email_token = str(uuid.uuid4())
                user.save()
                account_info(user=user,datejoined=timezone.now(),
                        user_token=secrets.token_urlsafe(), email_token=email_token).save()

                verification_link = 'https://' + str(get_current_site(request))+'/verify/'+email_token

                message = 'Please click this link to verify your email ' + verification_link
                
                send_email_token(email, email_token, message)
                
                return redirect('verify_email_page')

    return render(request,"sign_up.html")

def new_password_page(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            username = request.session['vschools_first_name'] + " " + request.session["vschools_last_name"]
            first_name = request.session['vschools_first_name'] 
            last_name = request.session["vschools_last_name"]
            #new_user=User.objects.create_user(username=username,email=request.session['vschools_email'],
                                        #password=request.POST['password2'])

            new_user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=request.session['vschools_email'],
                                        password=request.POST['password2'])
            new_user.save()

            account_info(user=new_user,datejoined=date.today()).save()

            user = authenticate(username=username,password=request.POST["password2"])

            if user is not None:
                login(request, user)
                del request.session["vschools_first_name"]
                del request.session["vschools_last_name"]
                del request.session["vschools_email"]
                return redirect("get_started") 
    return render(request,"new_password.html")

@login_required(login_url='login')
def person_info_page(request,user_token):
    user_id = account_info.objects.get(user_token=user_token).user.id
    person = account_info.objects.get(user=User.objects.get(id=user_id))

    context = {'person':person}

    return render(request,"person.html",context)

@login_required(login_url='login')
def share_screen_page(request):
    return render(request, 'share_screen.html')

def create_room(request):
    data = json.loads(request.body)
    uid = data['uid']
    room = data['room']
    Room(room_name=data['room'],uid=data['uid'],user=request.user,role='host').save()

def co_host_page(request,token_value):
    return render(request, "co-host.html")

@login_required(login_url='login')
def live_page(request):
    request.profile_picture = account_info.objects.get(user=request.user).profile_picture
    request.user_token = account_info.objects.get(user=request.user).user_token
    request.current_site = get_current_site(request)
    if request.method == "POST":
        data = json.loads(request.body)
        stream_title = data['stream_title']
        description = data['description']
        chats = data['chats']
        room_name = account_info.objects.get(user=request.user).user_token
        Room(room_name=room_name,chats=chats,title=stream_title,
                description=description,room_type='live').save()
    return render(request, "live.html")

def question_page(request):
    return render(request, "question.html")

def start_meeting_page(request):
    if request.method == "POST":
        print(request.POST)
    return render(request,"start_meeting.html")

def guest_page(request):
    return render(request, "guest.html")

@login_required(login_url='login')
def live_now(request):
    following = [account_info.objects.get(user=item.user).user_token for item in followings.objects.filter(follower=request.user)]
    ongoing = [item for item in Room.objects.all() if item.room_name in following]
    for item in ongoing:
        room_host = account_info.objects.get(user_token=item.room_name)
        item.host = room_host.user.username
        item.profile_picture = room_host.profile_picture
        item.users = Room_member.objects.filter(room=item).count()

    context = {'rooms':ongoing}
    return render(request, "live_now.html", context)

@login_required(login_url='login')
def meeting_auth(request, meeting_id):
    return render(request, 'meeting_auth.html')

@login_required(login_url='login')
def schedule_meeting(request):
    request.profile_picture = account_info.objects.get(user=request.user).profile_picture
    return render(request, 'schedule_meeting.html')

@login_required(login_url='login')
def meet_page(request, meeting_id):
    appId = '0eb3e08e01364927854ee79b9e513819'
    appCertificate = 'f2fdb8604d8b47a9bc71dcd5606f1d7e'
    channelName = meeting_id
    uid = request.user.id
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    room_messages = Room_message.objects.filter(room=Room.objects.get(room_name=meeting_id))

    for item in room_messages:
        item.user.profile_picture = account_info.objects.get(user=item.user).profile_picture

    context = {'profile_picture':account_info.objects.get(user=request.user).profile_picture,
                'host_profile_pic':account_info.objects.get(user_token=meeting_id).profile_picture,
                'meeting_link':'https://'+str(get_current_site(request))+'/meet/'+meeting_id,
                'host_username':account_info.objects.get(user_token=meeting_id).user.username,
                'token':token,'room_chats':room_messages}
    request.user.user_token = meeting_id
    request.meeting_description = Room.objects.get(room_name=meeting_id).description
    request.meeting_passcode = Room.objects.get(room_name=meeting_id).passcode
    if meeting_id == account_info.objects.get(user=request.user).user_token:
        context['role'] = 'host'
    else:
        context['role'] = 'participant'

    return render(request, "meet.html",context)

def join_meeting(request):
    return render(request, "join_meeting.html")

@login_required(login_url='login')
def home_page(request):
    if request.method == "POST":
        meeting_title = request.POST['meeting_title']
        Room.objects.filter(room_name=account_info.objects.get(user=request.user).user_token).delete()
        Room(room_name=account_info.objects.get(user=request.user).user_token,
            description = meeting_title.upper(), passcode = secrets.token_urlsafe(4), start_date=timezone.now()).save()
        return redirect('meet',account_info.objects.get(user=request.user).user_token)

    context = {'profile_picture':account_info.objects.get(user=request.user).profile_picture,
                'user_token':account_info.objects.get(user=request.user).user_token}
    return render(request, "home.html", context)

@login_required(login_url='login')
def watch_page(request, user_id):
    if user_id == account_info.objects.get(user=request.user).user_token:
        return redirect('home')
    request.profile_picture = account_info.objects.get(user=request.user).profile_picture
    user = account_info.objects.get(user_token=user_id).user
    following = request.user.id in [item.follower.id for item in followings.objects.filter(user=user)]
    room = Room.objects.get(room_name=user_id)
    context = {'following':following,'Room':room}

    if request.method == "POST":
        if request.user.id not in [item.follower.id for item in followings.objects.filter(user=user)]:
            followings(user=user,follower=request.user).save()
        else:
            followings.objects.get(user=user,follower=request.user).delete()

    return render(request, "watch.html",context)

@login_required(login_url='login')
def create_live(request):
    return render(request, "create_live.html")

@login_required(login_url='login')
def get_started_page(request):
    return render(request, "get_started.html")

def logout_user(request):
    logout(request)
    return redirect('login')

def test_page(request):
    appId = '0eb3e08e01364927854ee79b9e513819'
    appCertificate = 'f2fdb8604d8b47a9bc71dcd5606f1d7e'
    channelName = 'victor'
    uid = request.user.id
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    context = {'token':token}

    return render(request, "test.html",context)

def meeting_ended(request):
    return render(request, "meeting_ended.html")

def live_stream_ended(request):
    return render(request, "live_stream_ended.html")





