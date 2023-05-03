from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, StreamingHttpResponse
from main.models import (account_info, Room, Room_member, Room_message, 
        whiteboard_files, MeetingWhiteboard, RecordedFiles, Room_recording, scheduledmeeting)
from datetime import date, timedelta, datetime
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from .tasks import test_function
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
from aiortc import RTCPeerConnection, RTCSessionDescription

from django_celery_beat.models import PeriodicTask, CrontabSchedule



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
        user = authenticate(request=request,username=request.POST['username'],password=request.POST['password'])
        
        if user is not None:
            if account_info.objects.get(user=user).email_verified:
                login(request, user)
                return redirect('home')
            else:
                return redirect('verify_email_page')
        else:
            messages.info(request, "<i class = 'fas fa-exclamation-circle'></i> Wrong log in details")

    return render(request, "login.html")

def update_username(request):
    data = json.loads(request.body)
    username = data['username']
    user = User.objects.get(id=request.user.id)

    item = account_info.objects.get(user=user)
    item.username = username
    item.save()
    return JsonResponse({'username':username}, safe=False)

def update_password(request):
    data = json.loads(request.body)
    password_one = data['password_one']
    password_two = data['password_two']
    user = User.objects.get(id=request.user.id)
    
    if password_one == password_two:
        user.set_password(password_two)
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

def MeetingNotFound(request, meeting_id):
    return render(request, "MeetingNotFound.html")

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

def email_verified(request):
    return render(request, "email_verified.html")

def verify_email_page(request):
    return render(request, 'verify_email_page.html')

def welcome_page(request):
    return render(request, 'welcome.html')

def kickout_page(request):
    return render(request, 'kickout.html')

def verify_email(request, token):
    try:
        obj = account_info.objects.get(email_token=token)
        obj.email_verified = True
        obj.save()
        return redirect('email_verified')
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

                template = render_to_string('activate_email.html',{'domain':str(get_current_site(request)),
                        'email_token':email_token, 'username':last_name})

                email = EmailMessage(
                    'Please verify your e-mail',
                    template,
                    settings.EMAIL_HOST_USER,
                    [email]
                )
                
                email.fail_silently = False
                email.send()
                
                return redirect('verify_email_page')

    return render(request,"sign_up.html")

def scheduled_meetings(request):
    room = Room.objects.get(room_name=account_info.objects.get(user=request.user).user_token)
    meetings = scheduledmeeting.objects.filter(room=room)[::-1]
    context = {'meetings':meetings}
    return render(request, 'scheduled_meetings.html', context)

def scheduled_meeting(request, meeting_id):
    meeting = scheduledmeeting.objects.get(tokenValue=meeting_id)

    context = {'meetingTitle':meeting.meetingTitle, 'meetingDescription':meeting.meetingDescription,
                'start_date':meeting.start_date, 'start_time':meeting.start_time, 'meetingEndTime':meeting.MeetingEndTime,
                'invite_link':str(get_current_site(request))+'/scheduled-meeting/'+meeting_id,
                'daysOfWeek':json.loads(meeting.DaysOfWeek)}

    if meeting.WeeksOfMonth is not None:
        context['weeksOfMonth'] = json.loads(meeting.WeeksOfMonth)

    return render(request, 'scheduledMeeting.html', context)

@login_required(login_url='login')
def schedule_meeting(request):
    request.profile_picture = account_info.objects.get(user=request.user).profile_picture

    if request.method == 'POST':
        room = Room.objects.get(room_name=account_info.objects.get(user=request.user).user_token)
        meetingTitle = request.POST.get('meetingTitle')
        meetingDescription = request.POST.get('meetingDescription')
        frequency = request.POST['frequency']
        startDate = request.POST['startDate']
        startTime = request.POST['startTime']
        meetingEndingTime = request.POST['meetingEndTime']
        tokenValue = secrets.token_urlsafe()

        daysOfWeek = request.POST.get('daysOfWeek', None)
        weeksOfMonth = request.POST.get('weeksOfMonth', None)

        date_obj = datetime.strptime(startDate,'%Y-%m-%d').date()
        start_time_obj = datetime.strptime(startTime, '%H:%M').time()
        ending_time_obj = datetime.strptime(meetingEndingTime, '%H:%M').time()

        scheduledmeeting(room=room, meetingTitle=meetingTitle, meetingDescription=meetingDescription,
                        Frequency=frequency, start_date=date_obj, start_time=start_time_obj,
                        MeetingEndTime=ending_time_obj, DaysOfWeek=daysOfWeek, WeeksOfMonth=weeksOfMonth,
                        tokenValue=tokenValue).save()

        response = {'tokenValue':tokenValue}

        return JsonResponse(response, safe=False)


    return render(request, 'schedule_meeting.html')

def schedule_weekly_meeting(request):
    return render(request, "schedule_weekly_meeting.html")

def schedule_monthly_meeting(request):
    return render(request, "schedule_monthly_meeting.html")

@login_required(login_url='login')
def recorded_files(request):
    files = RecordedFiles.objects.filter(user=request.user)
    context = {'files':files}

    return render(request, 'recorded_files.html', context)

def meeting_recording(request):
    return render(request, 'meeting_recording.html')

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

    response = {'name':username,'profile_picture':profile_picture,
        'user_token':user_token,'uid':user.id,'hand_raised':room_member.hand_raised}

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
    request.roomId = Room.objects.get(room_id=meeting_id).id

    return render(request, "meeting.html",context)

def changeWhtieboardDetails(request):
    if request.method == 'POST':
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

    room = Room.objects.get(room_name=account_info.objects.get(user=request.user).user_token)
    meetings = scheduledmeeting.objects.filter(room=room)

    context = {'profile_picture':account_info.objects.get(user=request.user).profile_picture,
                'user_token':account_info.objects.get(user=request.user).user_token,'current_time':timezone.now(),
                'meetings':meetings}

    return render(request, "home.html", context) 

def start_meeting(request):
    if request.method == "POST":
        room = Room.objects.get(room_name=account_info.objects.get(user=request.user).user_token)
        room.room_id = secrets.token_urlsafe()
        room.passcode = secrets.token_urlsafe(4)
        room.start_date = timezone.now()
        room.save()
        return JsonResponse({'meeting_id':room.room_id}, safe=False)

def logout_user(request):
    logout(request)
    return redirect('login')

async def test_page(request):
    '''
    peerConnection = RTCPeerConnection()
    await peerConnection.createOffer()

    offer = peerConnection.localDescription
    print(offer)
    '''

    return render(request, "test.html")

def meeting_ended(request):
    return render(request, "meeting_ended.html")





