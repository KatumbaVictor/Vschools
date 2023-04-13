var video = document.createElement('video');
video.setAttribute('autoplay','');


var localDescription;
var UID = 9;
const roomId = 8;
var privateID = null;

Janus.init({
   debug: "all",
   callback: function () {
      console.log('initialized')
   }
})

var roomOptions = {
   request: 'create',
   room: Number(roomId),
   publishers: 100,
   bitrate: 128000,
   bitrate_cap: true,
   notify_joining: true,
   record: false,
   description: 'video room',
   require_pvtid: true
}

var janus = new Janus({
   //server: 'ws://localhost:8188/janus'
   server: `http://localhost:8088/janus`,
   iceServers: [{urls:"stun:stun.l.google.com:19302"}],
   success: function () {
      console.log('started')
      setTimeout(start(), 6000);
   },
   error: function(error) {
      console.log(error)
   }
})


let start = () => {
    janus.attach({
        plugin: "janus.plugin.videoroom",
        success: (handle) => {
            pluginHandle = handle;
            //Creating a video room
            handle.send({
                'message': { request: 'exists', 'room': Number(UID) },
                success: (response) => {
                    if (response['exists'] == true) {
                        var info = {'id':UID,'profile_picture':profile_picture,'name':username,
                            'user_token':user_token};
                        let register = {
                            request: "join",
                            room: response["room"],
                            ptype: "publisher",
                            display: JSON.stringify(info),
                            id: Number(UID)
                        };
                        handle.send({
                            "message": register
                        })
                    }else {
                        handle.send({
                            "message": roomOptions,
                            success: function (response) {
                                //Create SDP Offer
                                console.log(response)
                                let event = response["videoroom"];
                                if(event) {
                                    // Join the video room here
                                    var info = {'id':UID,'profile_picture':profile_picture,'name':username,
                                        'user_token':user_token}
                                    let register = {
                                        request: "join",
                                        room: response["room"],
                                        ptype: "publisher",
                                        display: JSON.stringify(info),
                                        id: Number(UID)
                                    };
                                    handle.send({ message: register });
                                    messagesocket = new WebSocket(MessageSocket);
                                    messagesocket.addEventListener('message',getSocketMessages);
                                }

                            }
                        })
                        
                    }
            }
         })
      },

    iceState: (state) => {
        console.log('state changed to', state);
    },

    mediaState: (medium, on, mid) => {
        console.log("Janus " + (on ? "started" : "stopped") + " receiving our " + medium + " (mid=" + mid + ")");
    },

    webrtcState: (on) => {
        console.log(`Peer connection state is ${(on ? "up" : "down")}  now`);
    },

    onlocaltrack: (track, added) => {
         // A local track to display has just been added (getUserMedia worked!) or removed
        localTracks.push(track);
        track.enabled = false;
        localStream.addTrack(track)
    },

      onremotetrack: (track, mid, added, metadata) => {
         // A remote track (working PeerConnection!) with a specific mid has just been added or removed
         // You can query metadata to get some more information on why track was added or removed
         // metadata fields:
         //   - reason: 'created' | 'ended' | 'mute' | 'unmute'
      },

      onmessage: (msg, jsep) => {
         console.log(msg)
         let event = msg["videoroom"];
         if (event) {
            if (event === 'joined') {
              privateID = msg["private_id"];
              pluginHandle.createOffer({
                 tracks: [
                       {type: 'audio', capture: true, recv: false},
                       {type: 'video', capture: true, recv: false},
                       {type: 'data'}
                    ],
                 success: (jsep) => {
                    
                 },
                 error: (error) => {
                    console.log(error);
                 }
              })

            }
         }

         if(jsep) {
            // Received an answer from the server
            pluginHandle.handleRemoteJsep({ jsep: jsep });
         }
      },
      error: (error) => {
         console.log(error)
      }
   })
}

let remoteFeed = (streams, display) => {
    var stream = new MediaStream();
    var subscription = [];
    var info = JSON.parse(display);
    janus.attach({
        plugin: "janus.plugin.videoroom",
        success: (handle) => {
            streams.forEach((item) => {
                subscription.push({feed: item.id, mid: item.mid});
            })

            let subscribe = {
               request: "join",
               room: roomId,
               ptype: "subscriber",
               streams: subscription,
               private_id: privateID
            };

            handle.send({ message: subscribe });

            var profile_picture = info.profile_picture;
            var id = info.id;
            var username = info.name;
            var user_token = info.user_token;

            handleJoinedUser({'name':username,'uid':id,'profile_picture':profile_picture,
                'user_token':user_token, 'stream': stream});
        },

        iceState: (state) => {
            console.log('state changed to ',state);
        },

        onremotetrack: (track, mid, added, metadata) => {
        // A remote track (working PeerConnection!) with a specific mid has just been added or removed
        // You can query metadata to get some more information on why track was added or removed
        // metadata fields:
        //   - reason: 'created' | 'ended' | 'mute' | 'unmute'
            var id = info.id;
            var mediaType = track.kind

            if (added) {
                UserPublishedEvent(id, mediaType);
                stream.addTrack(track);
            }else {
                UserUnpublishedEvent(id, mediaType);
            }
        },

        onmessage: (msg, jsep) => {
            if (jsep) {
                handle.createAnswer({
                    jsep: jsep,
                    tracks: [{type: 'data'}],

                    success: function(jsep) {
                        let body = { request: "start", room: roomId };
                        handle.send({ message: body, jsep: jsep });
                     },

                     error: function(error) {
                        console.log(error);
                     }
                })
            }
        }
    })
}