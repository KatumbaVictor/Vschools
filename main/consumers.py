import json
import asyncio
import time
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from main.models import Room, Room_member, account_info, Room_message, Room_recording
from django.utils import timezone
from agora_token_builder import RtcTokenBuilder

class MeetingRecording(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)
        self.accept()

        recording_item = Room_recording(room=Room.objects.get(room_id=self.room_name))
        recording_item.save()

    def disconnect(self, close_code):
        Room_recording.objects.get(room=Room.objects.get(room_id=self.room_name)).delete()
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)


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

    def user_info(self, event):
        data = json.loads(event['text'])
        self.send(text_data=json.dumps(data))

    