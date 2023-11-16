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
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webpush/', include('webpush.urls')),
    path('passkeys/', include('passkeys.urls')),
    path('webauthn-registration', webauthn_registration),
    path('webauthn-registration-complete/', webauthn_registration_complete),
    path('webauthn-verify/', webauthn_verify),
    path('webauthn-registration-options/',webauthn_registration_options),
    path('webauthn-authentication-options/',webauthn_authentication_options),
    path('webauthn-verify-registration/', verify_webauthn_registration),
    path('webauthn-authenticate/',webauthn_authentication),
    path('payments/', include('payments.urls')),
    path('chat/', include('vschoolschat.urls')),
    path('login/',login_page, name = "login"),
    path('', home_page, name = "home"),
    path('get_token/', getToken, name = "getToken"),
    path('verify-email/',verify_email_page, name = "verify_email_page"),
    path('update_username/',update_username),
    path('update_password/',update_password),
    path('logout/',logout_user, name = "logout"),
    path('sign-up/',sign_up_page, name = "sign_up"),
    path('about/', about_page, name = "about"),
    path('terms-of-service/', terms_of_service, name = "terms_of_service"),
    path('privacy-policy/', privacy_policy, name = "privacy_policy"),
    path('cookie-policy/', cookie_policy, name = "cookie_policy"),
    path('disclaimer/', disclaimer_page, name = "disclaimer"),
    path('settings/',settings_page, name = "settings"),
    path('schedule-meeting/', schedule_meeting, name = "schedule"),
    path('scheduled-meetings/', scheduled_meetings, name = "scheduled_meetings"),
    path('getRoomMember/', getRoomMember, name = "getRoomMember"),
    path('welcome/', welcome_page, name = "welcome"),
    path('kickout/', kickout_page),
    #url(r'^files', include('db_file_storage.urls')),
    path('join_session/', join_session, name = "join_session"),
    path('checkMeetingRecording/', checkMeetingRecording, name = "checkMeetingRecording"),
    path('scheduled-meeting/<str:meeting_id>', scheduled_meeting, name = "scheduledMeeting"),
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



handler404 = 'main.views.handle_404'