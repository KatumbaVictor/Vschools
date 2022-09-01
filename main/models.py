from django.db import models
from django.contrib.auth.models import User
from datetime import date



class account_info(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, unique=True)
    datejoined = models.DateField(blank=True)
    profile_picture = models.ImageField(blank=True, upload_to='profile_pics', default='no_profile_Pic.jpeg')
    description = models.TextField(blank=True)
    link = models.TextField(blank=True,null=True)
    user_token = models.TextField(unique=True)
    email_token = models.CharField(max_length=200, null=True, blank=True)
    email_verified = models.BooleanField(default=False)

class followings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")

class Room(models.Model):
    room_name = models.TextField(unique=True)
    chats = models.BooleanField(default=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    passcode = models.TextField(blank=True, null=True)
    room_type = models.CharField(max_length=30, default='meeting')
    start_date = models.DateTimeField(blank=True, null=True)

class Room_member(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=30)
    time_joined = models.DateTimeField(blank=True, null=True)

class Room_message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    time = models.DateTimeField()

class Raised_hands(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Attendence_report(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_joined = models.DateTimeField(blank=True, null=True)
    time_left = models.DateTimeField(blank=True, null=True)

class meeting_schedule(models.Model):
    uer = models.ForeignKey(User, on_delete=models.CASCADE)
    meeting_title = models.TextField()
    meeting_time = models.DateTimeField()


