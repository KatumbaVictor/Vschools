import json
import asyncio
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from main.models import Room, Room_member, account_info, Room_message, Raised_hands
from django.utils import timezone


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.uid = self.scope['url_route']['kwargs']['uid']
        self.role = self.scope['url_route']['kwargs']['role']
        Room_member(room=Room.objects.get(room_name=self.room_name),user=self.scope['user'],role=self.role,
                    time_joined=timezone.now()).save()
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.accept()
        room_participants = [{'name':item.user.username,'uid':item.user.id,'role':item.role,'user_joined':True,
            'profile_picture':account_info.objects.get(user=item.user).profile_picture.url} for item in Room_member.objects.filter(room=Room.objects.get(room_name=self.room_name))]
        
        for item in room_participants:
            async_to_sync(self.channel_layer.group_send)(
                self.room_name,
                {
                    'type':'user_info',
                    'text': json.dumps(item)
                }
        )

    def disconnect(self, close_code):
        try:
            room = Room.objects.get(room_name=self.room_name)
            Room_member.objects.filter(room=room,user=self.scope['user'],role=self.role).delete()
            if self.role == 'host':
                Room.objects.filter(room_name=self.room_name).delete()
        except:
            pass
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)

    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type':'chat_message',
                'text': text_data
            }
        )
        

    def chat_message(self, event):
        data = json.loads(event['text'])

        if 'raise_hand' in data:
            room = Room.objects.get(room_name=self.room_name)
            user = User.objects.get(id=int(data['id']))
            Raised_hands(room=room,user=user).save()
            data['hands'] = Raised_hands.objects.filter(room=room).count()
        
        if 'lower_hand' in data:
            room = Room.objects.get(room_name=self.room_name)
            user = User.objects.get(id=int(data['id']))
            Raised_hands.objects.get(room=room,user=user).delete()
            data['hands'] = Raised_hands.objects.filter(room=room).count()

        self.send(text_data=json.dumps(data))

    def user_info(self, event):
        data = json.loads(event['text'])
        self.send(text_data=json.dumps(data))

    
    


