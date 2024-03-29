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
    first_name = models.TextField(null=True, blank=True)
    last_name = models.TextField(null=True, blank=True)
    username = models.TextField(null=True, blank=True)
    webauthn_challenge = models.TextField(blank=True, null=True)

class Room(models.Model):
    room_name = models.TextField(unique=True)
    chats = models.BooleanField(default=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    passcode = models.TextField(blank=True, null=True)
    room_type = models.CharField(max_length=30, default='meeting')
    start_date = models.DateTimeField(blank=True, null=True)
    time_limit = models.IntegerField(default=2400)
    room_id = models.TextField(unique=True, null=True)

class Room_member(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    role = models.CharField(max_length=30)
    time_joined = models.DateTimeField(blank=True, null=True)
    hand_raised = models.BooleanField(default=False)

class Room_recording(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE, unique=True)

class Room_message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    room_member = models.ForeignKey(Room_member, on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    file = models.FileField(blank=True, null=True, upload_to='media')
    file_type = models.CharField(max_length=30, blank=True, null=True)
    file_name = models.TextField(blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)



class scheduledmeeting(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    meetingTitle = models.CharField(max_length=50)
    meetingDescription = models.CharField(max_length=50)
    Frequency = models.CharField(max_length=50)
    start_date = models.DateTimeField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    MeetingEndTime = models.TimeField(blank=True, null=True)
    DaysOfWeek = models.JSONField(blank=True, null=True)
    WeeksOfMonth = models.JSONField(blank=True, null=True)
    tokenValue = models.CharField(max_length=50, unique=True)


class MeetingWhiteboard(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    room_token = models.TextField(blank=True, null=True)
    room_uuid = models.TextField(blank=True, null=True)

class whiteboard_files(models.Model):
    room_name = models.TextField()
    file = models.FileField(upload_to='media')

class RecordedFiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fileUrl = models.TextField()

class credentials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.TextField()