var localDescription;

var uid = Number(2)
const roomId = 8;
var privateID = null;
var stream = new MediaStream();

var video = document.createElement('video');
video.setAttribute('autoplay','');
video.srcObject = stream;

Janus.init({
   debug: "all",
   callback: function () {
      console.log('initialized')
   }
})

var janus = new Janus({
   //server: 'ws://localhost:8188/janus'
   server: `http://localhost:8088/janus`,
   iceServers: [{urls:"stun:stun.l.google.com:19302"}],
   success: function () {
      start();
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
            let register = {
                request: "join",
                room: roomId,
                ptype: "subscriber",
                id: uid
            };
            handle.send({
                "message": register
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
    },

    onremotetrack: (track, mid, added, metadata) => {
         // A remote track (working PeerConnection!) with a specific mid has just been added or removed
         // You can query metadata to get some more information on why track was added or removed
         // metadata fields:
         //   - reason: 'created' | 'ended' | 'mute' | 'unmute'
        stream.addTrack(track);
    },

    onmessage: (msg, jsep) => {
        console.log(msg)
        let event = msg["videoroom"];
        if (event) {
            if (event === 'joined') {
                privateID = msg["private_id"];
                pluginHandle.createOffer({
                   tracks: [
                       {type: 'audio', capture: false, recv: true},
                       {type: 'video', capture: false, recv: true},
                       {type: 'data'}
                    ],
                    success: (jsep) => {
                    
                    },
                    error: (error) => {
                       console.log(error);
                    }
                })

                if (msg['publishers']) {
                    var list = msg["publishers"];
                    list.forEach((item) => {
                        var id = item['id'];
                        var streams = item['streams'];
                        var display = item['display'];
                        streams.forEach((stream) => {
                            stream['id'] = id;
                        })
                        remoteFeed(streams, display);
                    })
                }

            }else if (event === 'event') {
                if (msg["joining"]) {
                    // A user has joined the video room
                }else if (msg["publishers"]) {
                    var list = msg["publishers"];
                    list.forEach((item) => {
                        var id = item['id'];
                        var streams = item['streams'];
                        var display = item['display'];
                        streams.forEach((stream) => {
                            stream['id'] = id;
                        })
                        remoteFeed(streams, display);
                    })
                }else if (msg["leaving"]) {
                    // A user has left the video room
                    var user_id = msg["leaving"];
                    var holder = document.getElementById(msg['id'].toString());
                    holder.remove();
               }else if (msg['unpublished']) {
                  var user_id = msg["unpublished"];
               }
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