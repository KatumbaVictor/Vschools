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
from aiortc import (RTCPeerConnection, RTCSessionDescription, RTCConfiguration, RTCIceServer, RTCIceCandidate,
    RTCIceGatherer, RTCIceTransport, VideoStreamTrack)
from aiortc.contrib.media import MediaRelay
from django.conf import settings
from main.utils import *
import numpy
import secrets

peer_connections = []
relay = MediaRelay()

class SignalingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        iceServers = [RTCIceServer(urls='stun:stun.l.google.com:19302')]
        config = RTCConfiguration(iceServers=iceServers)
        config.sdpSemantics = "unified-plan"
        self.peerConnection = RTCPeerConnection(configuration=config)

        self.peerConnection.addTransceiver('audio')
        self.peerConnection.addTransceiver('video')

        self.peerConnection.on('negotiationneeded', self.on_negotiation_needed)
        self.peerConnection.on('icecandidate', self.on_ice_candidate)
        self.peerConnection.on('track',self.on_track)
        self.peerConnection.room_name = self.room_name

        peer = self.peerConnection
        peer_connections.append(peer)

    async def disconnect(self, close_code):
        await self.peerConnection.close()
        peer = self.peerConnection
        peer_connections.remove(peer)

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        
        if 'offer' in data:
            answer = await create_answer(self.peerConnection, data['offer'])
            print(answer)
            await self.send(json.dumps({'answer':answer}))
            '''
            candidates = await get_candidates()
            
            for candidate in candidates:
                sdp = "candidate:"+candidate.foundation+" "+str(candidate.component)+" "+candidate.protocol+" "+str(candidate.priority)+" "+candidate.ip+" "+str(candidate.port)+" typ "+candidate.type+" raddr "+str(candidate.relatedAddress)+" rport "+str(candidate.relatedPort) 
                print(sdp)
                candidate = {'candidate':sdp,'sdpMid':0}
                await self.send(json.dumps({'icecandidate':candidate}))
            '''
        if 'icecandidate' in data:
            await receive_icecandidate(self.peerConnection, data['icecandidate'])

        if 'new_offer' in data:
            answer = await create_new_answer(self.peerConnection, data['new_offer'])
            await self.send(json.dumps({'new_answer':answer}))

        if 'victor' in data:
            print(78)

            
    

    async def on_negotiation_needed(self):
        answer = await create_new_answer(self.peerConnection)
        await self.send(json.dumps({'new_answer':answer}))

    async def on_ice_candidate(self, event):
        candidate = event.candidate
        print(candidate)

    async def on_track(self, track):
        new_track = relay.subscribe(track)
        print(new_track)
        

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
            room_member.hand_raised = True
            room_member.save()

        if 'lower_hand' in data:
            user = User.objects.get(id=int(data['id']))
            room_member = Room_member.objects.get(room=room,user=user)
            room_member.hand_raised = False
            room_member.save()

    def user_info(self, event):
        data = json.loads(event['text'])
        self.send(text_data=json.dumps(data))

    