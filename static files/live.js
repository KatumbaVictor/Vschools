let conn = new WebSocket("ws://127.0.0.1:8000");

navigator.mediaDevices.getUserMedia({
    video: true
}).then(function(stream){
    document.querySelector('video').srcObject = stream;

    const configuration = {'iceServers': [{'urls': 'stun:stun.l.google.com:19302'}]}
    const peer = new RTCPeerConnection(configuration);
    stream.getTracks().forEach(track => peer.addTrack(track, stream));
    peer.createOffer()
    .then(offer => peer.setLocalDescription(offer))
})
