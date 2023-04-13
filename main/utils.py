import aiortc
from aiortc import (RTCPeerConnection, RTCSessionDescription, VideoStreamTrack, 
                MediaStreamTrack, RTCIceCandidate, RTCIceCandidate, RTCIceGatherer, RTCIceServer)
from aiortc.contrib.media import MediaRecorder
import asyncio
import secrets


async def get_candidates():
    iceServers = [RTCIceServer(urls='stun:stun.l.google.com:19302')]
    gatherer = RTCIceGatherer(iceServers=iceServers)
    await gatherer.gather()
    localCandidates = gatherer.getLocalCandidates()

    return localCandidates 


async def create_answer(peerConnection, offer):
    sessionDescription = RTCSessionDescription(sdp=offer['sdp'], type=offer['type'])
    await peerConnection.setRemoteDescription(sessionDescription)
    answer = await peerConnection.createAnswer()
    await peerConnection.setLocalDescription(answer)
    final_value = {'sdp':peerConnection.localDescription.sdp,'trickle':False,'type':'answer'}
    return final_value

async def create_new_answer(peerConnection, offer):
    sessionDescription = RTCSessionDescription(sdp=offer['sdp'], type=offer['type'])
    await peerConnection.setRemoteDescription(sessionDescription)
    final_value = {'sdp':peerConnection.localDescription.sdp,'type':'answer'}
    return final_value

async def receive_icecandidate(peerConnection: RTCPeerConnection, data):
    candidate_string = data['candidate']
    components = candidate_string.split(" ")

    if len(candidate_string) > 0:
        foundation = components[0][-1]
        component = components[1]
        protocol = components[2]
        priority = components[3]
        ip_address = components[4]
        port = components[5]
        connection_type = components[7]
        
        candidate = RTCIceCandidate(component=int(component),
                                    foundation=foundation,
                                    ip=ip_address,
                                    port=int(port),
                                    priority=int(priority), 
                                    protocol=protocol, 
                                    type=connection_type,
                                    sdpMid=data["sdpMid"],
                                    sdpMLineIndex=int(data['sdpMLineIndex']))

        await peerConnection.addIceCandidate(candidate)

async def record():
    print('recording function')
