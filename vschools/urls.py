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
    path('',guest_page, name = "guest"),
    path('login/',login_page, name = "login"),
    path('home/', home_page, name = "home"),
    path('get_started/', get_started_page, name = "get_started"),
    path('logout/',logout_user, name = "logout"),
    path('sign_up/',sign_up_page, name = "sign_up"),
    path('loading/',loading_page, name = "loading"),
    path('settings/',settings_page, name = "settings"),
    path('new_password/', new_password_page, name = "new_password"),
    path('ask_delete/',ask_delete_page, name = "ask_delete"),
    path('confirm_delete/',confirm_delete_page, name = "confirm_delete_page"),
    path('messages/', messages_page, name = "messages"),
    path('test/', test_page, name = "test"),
    path('posts/', new_posts_page, name = "posts"),
    path('notifications/', notifications_page, name = "notifications"),
    path('user_info/', user_info_page, name = "user_info"),
    path('groups/', groups_page, name = "groups"),
    path('live/', live_page, name = "live"),
    path('accept/', accept_page, name = "accept"),
    path('join/', join_meetings_page, name = "join_meeting"),
    path('follow/', follow_page, name = "follow"),
    path('saved/', saved_posts_page, name = "saved_posts"),
    path('group_media/', group_media_page, name = "group_media"),
    path('activities/', activities_page, name = "activities"),
    path('ads/',advertisements_page, name = "adverts"),
    path('meetings/', meetings_page, name = "meetings"),
    path('person/',person_info_page, name = "person_info"),
    path('comments/',comments_page, name = "comments"),
    path('reset',auth_views.PasswordResetView.as_view(template_name="forgot_password.html"), 
        name = "reset_password"),
    path('reset_sent/',
            auth_views.PasswordResetDoneView.as_view(template_name="email_verification.html"), 
            name = "password_reset_done"),
    path('reset/<uidb64>/<token>',
            auth_views.PasswordResetConfirmView.as_view(template_name="change_password.html"), 
            name = "password_reset_confirm"),
    path('reset_complete',
            auth_views.PasswordResetCompleteView.as_view(template_name="password_changed.html"), 
            name = "password_reset_complete")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
