from django.db import models
from django.contrib.auth.models import User
from datetime import date

class account_info(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    datejoined = models.DateField()
    profile_picture = models.ImageField(blank=True, upload_to='profile_pics')

class posts(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField()
    caption = models.TextField(blank=True)
    file_uploaded = models.FileField(blank=True, upload_to='posts')
    text_post = models.TextField(blank=True)
    likes = models.IntegerField(default=0)
    reactions = models.IntegerField(default=0)
    comments = models.TextField(default=0)

class messaging(models.Model):
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    date = models.DateField()
    sender = models.BooleanField()
    message_info = models.TextField()

class notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    notification = models.TextField()

class saved_posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(posts, on_delete=models.CASCADE)



