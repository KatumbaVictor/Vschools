import json
import asyncio
import time
import os
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from main.models import Room, Room_member, account_info, Room_message, Room_recording
from django.utils import timezone
from django.conf import settings
from main.utils import *
import numpy
import secrets
import base64

class DialogueConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        if text_data:
            async_to_sync(self.channel_layer.group_send)(
                self.room_name,
                {
                    'type':'chat_message',
                    'text': text_data
                }
            )

        if bytes_data:
            async_to_sync(self.channel_layer.group_send)(
                self.room_name,
                {
                    'type':'send_binary',
                    'text': bytes_data
                }
            )

    def send_binary(self, event):
        self.send(bytes_data=event['text'])

    def chat_message(self, event):
        data = json.loads(event['text'])
        self.send(text_data=json.dumps(data))

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_name']
        room = Room.objects.get(room_id=self.room_id)
        room_member = Room_member(room=room,user=self.scope['user'],
            role='participant',time_joined=timezone.now())
        room_member.save()
        async_to_sync(self.channel_layer.group_add)(self.room_id, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        room = Room.objects.get(room_id=self.room_id)
        Room_member.objects.filter(room=room,user=self.scope['user']).delete()
        async_to_sync(self.channel_layer.group_discard)(self.room_id, self.channel_name)

    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_id,
            {
                'type':'chat_message',
                'text': text_data
            }
        )

    def chat_message(self, event):
        data = json.loads(event['text'])
        self.send(text_data=json.dumps(data))
        room = Room.objects.get(room_id=self.room_id)

        if 'message' in data:
            user = User.objects.get(id=int(data['id']))
            room_member = Room_member.objects.get(room=room,user=user)
            Room_message(room=room,room_member=room_member,
                message=data['message'],time=timezone.now()).save()

        if 'raise_hand' in data:
            user = User.objects.get(id=int(data['id']))
            room_member = Room_member.objects.get(room=room,user=user)
            #room_member.hand_raised = True
            room_member.save()

        if 'lower_hand' in data:
            user = User.objects.get(id=int(data['id']))
            room_member = Room_member.objects.get(room=room,user=user)
            #room_member.hand_raised = False
            room_member.save()

    def user_info(self, event):
        data = json.loads(event['text'])
        self.send(text_data=json.dumps(data))

    