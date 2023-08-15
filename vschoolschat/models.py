from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ChatUser(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE, unique=True)
	room_name = models.TextField()
	time_joined = models.DateTimeField()