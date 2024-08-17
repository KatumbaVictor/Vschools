from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, StreamingHttpResponse
from main.models import (account_info, Room, Room_member, Room_message, 
        whiteboard_files, MeetingWhiteboard, RecordedFiles, Room_recording, scheduledmeeting, credentials)
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
import os
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from webauthn import *






meta = {
        'url': 'https://careerconnect.com',
        'description': 'page description',
        'site_name':'Career Connect',
        'use_og': True,
        'use_twitter': True,
        'use_facebook': True,
        'use_schemaorg': True,
        'title':'Career connect home.',
        'locale':'en_US',
        'schemaorg_title': 'Career connect home page.',
        'object_type': 'website',
        'og_title':'Career connect home',
        'image': {
            'url':'https://careerconnect.com',
            'type':'some/mime',
            'width': 100,
            'height': 100,
            'alt': 'Career Connect Media'
        }
    }


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

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect username or password, Please check your credentials and try again, If you continue to have trouble, consider resetting your password.')

    return render(request, 'login.html')

@login_required(login_url='login')
def settings_page(request):
    context = {'meta':meta}

    return render(request,"settings_page.html",context)

def handle_404(request, exception):
    return render(request, 'error-pages/404.html', status=404)

def handle_500(request):
    return render(request, 'error-pages/500.html', status=500)

def handle_403(request, reason=""):
    return render(request, 'error-pages/403.html', {"reason": reason}, status=403)

def email_verified(request):
    return render(request, "email_verified.html")

def verify_email_page(request):
    return render(request, 'verify_email_page.html')

def welcome_page(request):
    return render(request, 'welcome.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def about_page(request):
    return render(request, 'about.html')

def terms_of_service(request):
    return render(request, 'terms_of_service.html')

def community_guidelines(request):
    return render(request, 'community_guidelines.html')

def cookie_policy(request):
    return render(request, 'cookie_policy.html')

def disclaimer_page(request):
    return render(request, 'disclaimer.html')

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
        print(request.POST)

    return render(request,"sign_up.html")

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

@login_required(login_url='login')
def home_page(request):
    context = {'meta':meta}

    return render(request, "home.html", context) 

def billing_page(request):
    return render(request, 'settings-pages/billing.html')

def contact_page(request):
    context = {'meta':meta}
    return render(request, "contact.html", context)

def community_forum(request):
    return render(request, 'forum.html')

def pricing_page(request):
    return render(request, 'pricing.html')

def services_page(request):
    return render(request, 'services.html')

def FAQ_page(request):
    return render(request, 'FAQ.html')

@login_required(login_url='login')
def webauthn_verify(request):
    return render(request, 'webauthn-verify.html')

@login_required(login_url='login')
def webauthn_registration(request):
    return render(request, 'webauthn-registration.html')

@login_required(login_url='login')
def webauthn_registration_complete(request):
    return render(request, 'webauthn-registration-complete.html')

def test_page(request):
    return render(request, "test.html")

def guest_page(request):
    return render(request, "guest.html")

def webauthn_registration_options(request):
    item=generate_registration_options(rp_id=settings.FIDO_SERVER_ID,rp_name='Vschools Meet',user_id=str(request.user.id),
                                    user_name=account_info.objects.get(user=request.user).username)

    registration_response = json.loads(options_to_json(item))

    target_user = account_info.objects.get(user=request.user)
    target_user.webauthn_challenge = registration_response['challenge']
    target_user.save()

    return JsonResponse({'publicKey':registration_response}, safe=False)

def verify_webauthn_registration(request):
    data = request.POST
    print(data)
    user = account_info.objects.get(user=request.user)

    item = verify_registration_response(credential=json.loads(data['credential']),expected_challenge=base64url_to_bytes(user.webauthn_challenge),expected_rp_id=settings.FIDO_SERVER_ID,
                                expected_origin='https://'+settings.FIDO_SERVER_ID,require_user_verification=True)
    print(item)

def webauthn_authentication_options(request):
    item=generate_authentication_options(rp_id=settings.FIDO_SERVER_ID)
    return JsonResponse({'publicKey':json.loads(options_to_json(item))}, safe=False)

def webauthn_authentication(request):
    data = json.loads(request.body)
    user = account_info.objects.get(user=request.user)

    item = verify_authentication_response(credential=base64url_to_bytes(data['credential']),expected_challenge=user.webauthn_challenge,expected_rp_id=settings.FIDO_SERVER_ID,
                                    expected_origin='https://'+settings.FIDO_SERVER_ID,credential_public_key=data['credential']['publicKey'],
                                    credential_current_sign_count=1,require_user_verification=True)
    print(item)

def user_logout(request):
    logout(request)
    return redirect('login')