"""vschools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',login_page, name = "login"),
    path('', home_page, name = "home"),
    path('get_token/', getToken, name = "getToken"),
    path('verify-email/',verify_email_page, name = "verify_email_page"),
    path('new-peerconnection/',newPeer),
    path('update_username/',update_username),
    path('update_password/',update_password),
    path('logout/',logout_user, name = "logout"),
    path('schedule-monthly-meeting/', scheduleMonthlyMeeting, name = "schedule_monthly_meeting"),
    path('schedule-annual-meeting/', scheduleAnnualMeeting, name = "schedule_annual_meeting"),
    path('schedule-onetime-meeting/', scheduleOneTimeMeeting, name = "schedule_onetime_meeting"),
    path('sign-up/',sign_up_page, name = "sign_up"),
    path('settings/',settings_page, name = "settings"),
    path('schedule-meeting/', schedule_meeting, name = "schedule"),
    path('getRoomMember/', getRoomMember, name = "getRoomMember"),
    path('join_session/', join_session, name = "join_session"),
    path('checkMeetingRecording/', checkMeetingRecording, name = "checkMeetingRecording"),
    path('scheduledMeeting/<str:meeting_id>', scheduledMeeting, name = "scheduledMeeting"),
    path('meeting_ended/',meeting_ended, name = "meeting_ended"),
    path('whiteboardDetails/', whiteboardDetails, name = "whiteboardDetails"),
    path('start_meeting/',start_meeting, name = "start_meeting"),
    path('changeWhiteboardDetails/', changeWhtieboardDetails, name = "changeWhtieboardDetails"),
    path('MeetingNotFound/<str:meeting_id>',MeetingNotFound),
    path('UpdateWhiteboardDetails/', UpdateWhiteboardDetails),
    path('recorded_meetings/', recorded_files, name = "recorded_files"),
    path('email-verified/',email_verified, name = "email_verified"),
    path('meeting_recording/', meeting_recording, name = "meeting_recording"),
    path('verify-email/<str:token>',verify_email),
    path('test/', test_page, name = "test"),
    path('meet/<str:meeting_id>',meet_page, name = "meet"),
    path('reset',auth_views.PasswordResetView.as_view(template_name="forgot_password.html"), 
        name = "reset_password"),
    path('reset_sent/',
            auth_views.PasswordResetDoneView.as_view(template_name="reset_sent.html"), 
            name = "password_reset_done"),
    path('reset/<uidb64>/<token>',
            auth_views.PasswordResetConfirmView.as_view(template_name="change_password.html"), 
            name = "password_reset_confirm"), 
    path('reset_complete',
            auth_views.PasswordResetCompleteView.as_view(template_name="reset_complete.html"), 
            name = "password_reset_complete")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



