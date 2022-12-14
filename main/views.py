from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import JsonResponse
from main.models import (account_info, Room, Room_member, Room_message, 
        whiteboard_files, MeetingWhiteboard, RecordedFiles, Room_recording)
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
import base64
import http.client
import boto3
import os


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
        return JsonResponse({'meeting_id':Room.objects.get(passcode=passcode).room_id}, safe=False)
    else:
        return JsonResponse({'not_found':True}, safe=False)
    

def checkMeetingRecording(request):
    data = request.GET
    room_id = data['room_id']
    room = Room.objects.get(room_id=room_id)
    if any(Room_recording.objects.filter(room=room)):
        return JsonResponse({'MeetingRecording':True}, safe=False)
    else:
        return JsonResponse({'MeetingRecording':False}, safe=False)

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

def update_username(request):
    data = json.loads(request.body)
    first_name = data['first_name']
    last_name = data['last_name']
    username = first_name + ' ' + last_name
    user = User.objects.get(id=request.user.id)
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    item = account_info.objects.get(user=user)
    item.first_name = first_name
    item.last_name = last_name
    item.username = username
    item.save()
    return JsonResponse({'first_name':first_name,'last_name':last_name,'username':username}, safe=False)

def update_password(request):
    data = json.loads(request.body)
    current_password = data['current_password']
    password_one = data['password_one']
    password_two = data['password_two']
    user = User.objects.get(id=request.user.id)
    
    if password_one == password_two:
        user.set_password('password_two')
        user.save()
    
    return JsonResponse({'password_changed':True})

def whiteboardDetails(request):
    data = request.GET
    room_name = data['room_name']
    room = Room.objects.get(room_id=room_name)
    item = MeetingWhiteboard.objects.get(room=room)
    response = None

    if item.room_token != None and item.room_uuid != None:
        response = {'room_token':item.room_token,'room_uuid':item.room_uuid}
    else:
        response = {}

    return JsonResponse(response, safe=False)

def UpdateWhiteboardDetails(request):
    return JsonResponse({'updated':True}, safe=False)

@login_required(login_url='login')
def settings_page(request):
    user = request.user
    context = {'user':user}
    user.token = account_info.objects.get(user=user).user_token
    user.username = account_info.objects.get(user=request.user).username

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
                user = User.objects.create_user(email,email,password_two)
                user.first_name = first_name
                user.last_name = last_name
                email_token = str(uuid.uuid4())
                user.save()
                account_info(user=user,datejoined=timezone.now(),
                        user_token=secrets.token_urlsafe(), email_token=email_token,
                        first_name=first_name,last_name=last_name,username=username).save()
                room = Room(room_name=account_info.objects.get(user=user).user_token)
                room.save()
                MeetingWhiteboard(room=room).save()

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
def schedule_meeting(request):
    request.profile_picture = account_info.objects.get(user=request.user).profile_picture
    return render(request, 'schedule_meeting.html')

@login_required(login_url='login')
def recorded_files(request):
    files = RecordedFiles.objects.filter(user=request.user)
    context = {'files':files}

    return render(request, 'recorded_files.html', context)

def meeting_recording(request, meeting_id):
    print("meeting id is "+meeting_id)
    room = Room.objects.get(room_id=meeting_id)
    room_members = Room_member.objects.filter(room=room)

    for item in room_members:
        item.username = account_info.objects.get(user = item.user).username
        item.profile_picture = account_info.objects.get(user=item.user).profile_picture

    context = {'room_members':room_members}

    return render(request, 'meeting_recording.html',context)

def getRoomMember(request):
    data = request.GET
    room_id = data['room_id']
    user_id = data['uid']

    user = User.objects.get(id=user_id)
    room = Room.objects.get(room_id=room_id)
    room_member = Room_member.objects.get(room=room, user=user)
    profile_picture = account_info.objects.get(user=user).profile_picture.url

    user_token = account_info.objects.get(user=user).user_token
    username = account_info.objects.get(user=user).username

    response = {'name':username,'profile_picture':profile_picture,'user_token':user_token,'uid':user.id}

    return JsonResponse(response, safe=False)


@login_required(login_url='login')
def meet_page(request, meeting_id):
    if not Room.objects.filter(room_id=meeting_id).exists():
        return redirect('home')

    appId = '0eb3e08e01364927854ee79b9e513819'
    appCertificate = 'f2fdb8604d8b47a9bc71dcd5606f1d7e'

    channelName = meeting_id
    expirationTimeInSeconds = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, request.user.id, role, privilegeExpiredTs)

    user_details = {}

    user_details['profile_picture'] = account_info.objects.get(user=request.user).profile_picture

    if request.method == 'POST':
        if request.FILES:
            if request.user.is_authenticated:
                room = Room.objects.get(room_id=meeting_id)
                room_member = Room_member.objects.get(id=int(request.POST['uid']))
                item = Room_message(room=room,room_member=room_member,
                    file=request.FILES['image'],file_type=request.POST['fileType'],
                    file_name=request.POST['fileName'],time=timezone.now())
                item.save()
                return JsonResponse({'fileUrl':item.file.url}, safe=False)
        else:
            try:
                video_file_name = request.POST['video_file_name']

                RecordedFiles(User=request.user, fileUrl=video_file_name).save()
            except:
                pass

    customer_key = "a0a3bcfe4bf24cb48e5ace72855058cc"
    customer_secret = "35c8f03349184c40932e03d531c06de5"
    credentials = customer_key + ":" + customer_secret
    base64_credentials = base64.b64encode(credentials.encode("utf8"))
    credential = base64_credentials.decode("utf8")

    room_chats = Room_message.objects.filter(room=Room.objects.get(room_id=meeting_id))
    room_name = Room.objects.get(room_id=meeting_id).room_name
    print(Room.objects.get(room_id=meeting_id).start_date)

    for item in room_chats:
        item.profile_picture = account_info.objects.get(user=item.room_member.user).profile_picture
        item.username = account_info.objects.get(user=item.room_member.user).username

    context = {'profile_picture':account_info.objects.get(user=request.user).profile_picture.url,
                'meeting_link':'https://'+str(get_current_site(request))+'/meet/'+meeting_id,
                'authorization': credential,'room_chats':room_chats, 'token':token}

    request.user.username = account_info.objects.get(user=request.user).username
    request.user.user_token = account_info.objects.get(user=request.user).user_token
    request.meeting_description = Room.objects.get(room_id=meeting_id).description
    request.meeting_passcode = Room.objects.get(room_id=meeting_id).passcode
    request.room_name = room_name

    return render(request, "meeting.html",context)

def changeWhtieboardDetails(request):
    if request.method == 'POST':
        if request.is_ajax:
            data = json.loads(request.body)
            room = Room.objects.get(room_id=data['room_id'])
            item = MeetingWhiteboard.objects.get(room=room)
            item.room_token = data['room_token']
            item.room_uuid = data['room_uuid']
            item.save()
            return render(request, 'meeting.html')

@login_required(login_url='login')
def home_page(request):
    request.user.username = account_info.objects.get(user=request.user).username

    context = {'profile_picture':account_info.objects.get(user=request.user).profile_picture,
                'user_token':account_info.objects.get(user=request.user).user_token,'current_time':timezone.now()}
    return render(request, "home.html", context) 

def start_meeting(request):
    if request.method == "POST":
        room = Room.objects.get(room_name=account_info.objects.get(user=request.user).user_token)
        room.room_id = secrets.token_urlsafe()
        room.passcode = secrets.token_urlsafe(4)
        room.start_date = timezone.now()
        room.save()
        return JsonResponse({'meeting_id':room.room_id}, safe=False)

@login_required(login_url='login')
def get_started_page(request):
    return render(request, "get_started.html")

def logout_user(request):
    logout(request)
    return redirect('login')

def test_page(request):
    x_forw_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip_address = None

    if x_forw_for is not None:
        ip_address = x_forw_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    print(ip_address)

    return render(request, "test.html")

def meeting_ended(request):
    return render(request, "meeting_ended.html")





