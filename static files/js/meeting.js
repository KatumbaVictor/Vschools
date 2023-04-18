if (navigator.mediaDevices.getDisplayMedia == undefined){document.getElementById('controls').children[3].remove()};
const UID = document.getElementById('container').dataset.id;
const username = document.getElementById('main').dataset.username;
const profile_picture = document.getElementById('controls').dataset.profile_picture;
const notifications = document.getElementById('notifications');
const container = document.getElementById('container'); 
const room_name = document.getElementById('controls').dataset.room_name;
const expression = /((ftp|http|https):\/\/)(www\.)?([\w]+)(\.[\w]+)+(\/[\w]+)*/g;
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const localStream = new MediaStream();
var CHANNEL = window.location.pathname.split('/')[2];
var connection_protocol;
var all_hands = document.getElementById('all_hands');
var chats = false;
var set_captions = false;
var connection;
var messagesocket;
var sid;
var time_string;
var video_track_playing = false; 
var audio_track_playing = false; 
var time_limit;
var room;
var user_token = document.getElementById('meeting_info').dataset.user_token;
var whiteboard;
var all_users = 0;
var recording = false;
var MessageSocket;
var pluginHandle;
var localTracks = [];

var videoTrack;
var audioTrack;
var screenTrack;

var comment_holder = document.getElementById('livechat').children[1];
comment_holder.scrollTop = comment_holder.scrollHeight;


var file_types = ['audio/mpeg','audio/wav','application/pdf','image/jpeg','image/png','video/mp4',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];

var send_notification = (title, body) => {
    if (expression.test(body) == true) {
        body = body.replace(expression, (url) => {
            return `<a href = '${url}' target="_blank">${url}</a>`;
        })
    }
    var notification = document.getElementById('notification');
    var message = `<span>${title}</span> ${body}`;
    notification.innerHTML = message;
    notification.setAttribute('data-message',JSON.stringify(message));
    notification.style.display = "block";

    setTimeout(() => {
        notification.style.opacity = '1';
    }, 180)

    setTimeout(() => {
        if (notification.dataset.message == JSON.stringify(message)) {
            notification.style.opacity = '0';
            setTimeout(() => {
                notification.style.display = "none";
            }, 1000)
        }
    } ,5000)
}

let getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== ''){
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')){
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


if (window.location.protocol == 'https:'){
    connection_protocol = 'wss';
    MessageSocket = `${connection_protocol}://${window.location.host}:8001/MessageSocket/${CHANNEL}/`;
}else {
    connection_protocol = 'ws';
    MessageSocket = `${connection_protocol}://${window.location.host}/MessageSocket/${CHANNEL}/`;
}

let joinAndDisplayLocalStream = async () => {

    Array.from(document.getElementsByTagName('button')).forEach(item => {
        if (item.hasAttribute('disabled')){
            item.removeAttribute('disabled');
        }
    })
}

let UserUnpublishedEvent = (uid, mediaType) => {
    var holder = document.getElementById(uid.toString());
    var video = document.getElementById(`video_${uid.toString()}`);

    if (mediaType == 'video'){
        video.style.visibility = "hidden";
        var profile_picture = document.getElementById(`profile_picture_${uid.toString()}`);
        profile_picture.style.display = "block";
    }else {
        var name = document.getElementById(`name_${uid.toString()}`);
        var microphone = name.firstElementChild;
        microphone.setAttribute('class','fas fa-microphone-slash');
        microphone.style.color = "red";
    }
}

let handleJoinedUser = (item) => {
    var name = document.createElement('p');
    name.setAttribute('id',`name_${item.uid.toString()}`);
    name.setAttribute('class','name')
    name.innerHTML = `<i class = 'fas fa-microphone-slash'></i> ${item.name} <span></span>`;

    var profile_picture = document.createElement('img');
    profile_picture.setAttribute('id',`profile_picture_${item.uid.toString()}`);
    profile_picture.setAttribute('src',item.profile_picture);

    var hand = document.createElement('p');
    hand.setAttribute('id',`hand_${item.uid.toString()}`);
    hand.setAttribute('class','hand');
    hand.innerHTML = '<i class = "fas fa-hand-paper"></i>';

    var holder = document.createElement('div');
    holder.setAttribute('id',item.uid.toString());
    holder.setAttribute('class','holder');
    holder.setAttribute('ondblclick','full_screen(this)');

    var video = document.createElement('video');
    video.setAttribute('autoplay','');
    video.setAttribute('muted','muted');
    video.setAttribute('id',`video_${item.uid.toString()}`);

    if (item.user_token == room_name) {
        document.getElementById('hosts').prepend(holder);
        name.innerHTML = `<i class = 'fas fa-microphone-slash'></i> ${item.name} <span>(meeting host)</span>`;
    }else {
        document.getElementById('hosts').appendChild(holder)
    }

    all_users = document.getElementById('hosts').children.length
    document.getElementById('meeting_tools').firstElementChild.innerHTML = `classroom (${all_users})`;

    holder.appendChild(name);
    holder.appendChild(profile_picture);
    holder.appendChild(hand);
    holder.appendChild(video);

    Janus.attachMediaStream(video, item.stream);

    if (item.hand_raised == true) {
        hand.style.opacity = "1";
    }

    var loader = container.firstElementChild;

    var player = holder.lastElementChild;
    
    player.style.display = "flex";
    player.style.flexDirection = "column";
    player.style.alignItems = "center";
    player.style.justifyItems = "center";

    var loader = container.firstElementChild;

    if (loader.getAttribute('class') == "loader_holder"){
        loader.remove();
    }

    /*Array.from(document.getElementsByClassName('holder')).forEach((item) => {
        item.style.width = "270px";
        item.style.height = "270px";
    })
    */
}

let UserPublishedEvent = (uid, mediaType) => {
    var holder = document.getElementById(uid.toString());
    var video = document.getElementById(`video_${uid.toString()}`);

    if (holder == null || video == null) {
        setTimeout(UserPublishedEvent(uid, mediaType), 2000);
    }else {
        if (mediaType === 'video'){
            var player = holder.lastElementChild;
            var video = holder.lastElementChild.firstElementChild;
            var image = document.getElementById(`profile_picture_${uid.toString()}`);
            image.style.display = "none";
            
            player.style.display = "flex";
            player.style.flexDirection = "column";
            player.style.alignItems = "center";
            player.style.justifyItems = "center";
            if (video != null) {
                video.style.visibility = "visible";
            }
        }

        if (mediaType === 'audio'){
            var name = document.getElementById(`name_${uid.toString()}`);
            var microphone = name.firstElementChild;
            microphone.setAttribute('class','fas fa-microphone');
            microphone.style.color = "blue";
        }
    }
}

let handleUserLeft = (uid) => {
    document.getElementById(uid.toString()).remove();

    all_users = document.getElementById('hosts').children.length
    document.getElementById('meeting_tools').firstElementChild.innerHTML = `classroom (${all_users})`;
}

let leaveAndRemoveLocalStream = async () => {
    window.open('/','_self');
}

function getImage() {
    document.getElementById('photo').click();
}

function sendFile(self) {
    if (self.files) {
        var item = {'profile_picture':profile_picture,'id':UID,
        'name':username,'fileType':self.files[0].type,'fileName':self.files[0].name};
    }
}

let getCurrentTime = () => {
    var date = new Date();
    var hours = date.getHours();
    var minutes = date.getMinutes();
    if (minutes < 10){
        minutes = '0'+minutes;
    }
    if (hours < 10){
        hours = '0'+hours;
    }

    var time = `${hours}:${minutes}`;

    return time;
}

let add_to_chat = (profile_picture, name, message) => {
    var time = getCurrentTime();
    var comment_holder = document.getElementById('livechat').children[1];

    if (expression.test(message) == true) {
        message = message.replace(expression, (url) => {
            return `<a href = '${url}' target="_blank">${url}</a>`;
        })
    }

    var container = `
        <div class = "message_container">
            <img class = 'profile_picture' src = "${profile_picture}"/>
            <p class = "user_name">${name} <span>${time}</span></p>
            <p class = "message">${message}</p>
        </div>
    `
    comment_holder.innerHTML += container;
    comment_holder.scrollTop = comment_holder.scrollHeight;
}

let getSocketMessages = function(self){
    var response = JSON.parse(self.data);
    var comment_holder = document.getElementById('livechat').children[1];

    if (response.message) {
        add_to_chat(response.profile_picture, response.name, response.message);

        if (chats === false) {
            send_notification(response.name, response.message);
        }
    }else if(response.lower_hand) {
        document.getElementById(`hand_${response.id.toString()}`).style.opacity = "0";
    }else if (response.raise_hand) {
        if (response.id == UID) {
            send_notification('<i class = "fas fa-hand-paper"></i> You','are raising a hand');
            add_to_chat(response.profile_picture, username, '<i class = "fas fa-hand-paper"></i> You are raising a hand');

        }else {
            send_notification(`<i class = "fas fa-hand-paper"></i> ${response.username}`,'is raising a hand');
            add_to_chat(response.profile_picture, response.username, '<i class = "fas fa-hand-paper"></i> is raising a hand');
        }

        document.getElementById(`hand_${response.id.toString()}`).style.opacity = "1";
    }else if (response.screen_sharing) {
        if (response.id == UID) {
            send_notification('You', 'have started screen sharing');
        }else {
            send_notification(response.username, 'has started screen sharing');
        }
    }else if (response.fileType) {
        var container = document.createElement('div');
        var time = getCurrentTime();
        var container;

        if (response.fileType == 'image/jpeg' || response.fileType == 'image/png') {
            var container = `
                <div class = "message_container">
                    <img class = 'profile_picture' src = "${response.profile_picture}"/>
                    <p class = "user_name">${response.name} <span>${time}</span></p>
                    <div class = "file_container">
                        <i class = "fas fa-file-image"></i>
                        <div>
                            <a target = "_blank" href = "${response.fileUrl}">${response.fileName}</a>
                        </div>
                    </div>
                </div>
            `
        }else if (response.fileType == 'video/mp4') {
            container = `
                <div class = "message_container">
                    <img class = 'profile_picture' src = "${response.profile_picture}"/>
                    <p class = "user_name">${response.name} <span>${time}</span></p>
                    <div class = "file_container">
                        <i class = "fas fa-file-video"></i>
                        <div>
                            <a target = "_blank" href = "${response.fileUrl}">${response.fileName}</a>
                        </div>
                    </div>
                </div>
            `
        }else if (response.fileType == 'audio/wav' || response.fileType == 'audio/mpeg') {
            container = `
                <div class = "message_container">
                    <img class = 'profile_picture' src = "${response.profile_picture}"/>
                    <p class = "user_name">${response.name} <span>${time}</span></p>
                    <div class = "file_container">
                        <i class = "fas fa-file-audio"></i>
                        <div>
                            <a target = "_blank" href = "${response.fileUrl}">${response.fileName}</a>
                        </div>
                    </div>
                </div>
            `
        }else if (response.fileType == 'application/pdf') {
            container = `
                <div class = "message_container">
                    <img class = 'profile_picture' src = "${response.profile_picture}"/>
                    <p class = "user_name">${response.name} <span>${time}</span></p>
                    <div class = "file_container">
                        <i class = "fas fa-file-pdf"></i>
                        <div>
                            <a target = "_blank" href = "${response.fileUrl}">${response.fileName}</a>
                        </div>
                    </div>
                </div>
            `
        }else if (response.fileType == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
            container = `
                <div class = "message_container">
                    <img class = 'profile_picture' src = "${response.profile_picture}"/>
                    <p class = "user_name">${response.name} <span>${time}</span></p>
                    <div class = "file_container">
                        <i class = "fas fa-file-word"></i>
                        <div>
                            <a target = "_blank" href = "${response.fileUrl}">${response.fileName}</a>
                        </div>
                    </div>
                </div>
            `
        }else if (response.fileType == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
            container = `
                <div class = "message_container">
                    <img class = 'profile_picture' src = "${response.profile_picture}"/>
                    <p class = "user_name">${response.name} <span>${time}</span></p>
                    <div class = "file_container">
                        <i class = "fas fa-file-excel"></i>
                        <div>
                            <a target = "_blank" href = "${response.fileUrl}">${response.fileName}</a>
                        </div>
                    </div>
                </div>
            `
        }

        comment_holder.innerHTML += container;
        comment_holder.scrollTop = comment_holder.scrollHeight;

        if (chats === false) {
            send_notification(response.name, 'shared a file');
        }
    }
}

let handle_camera = (self) => {
    var holder = document.getElementById(UID.toString());
    var profile_picture = document.getElementById(`profile_picture_${UID.toString()}`);
    var video = document.getElementById(`video_${UID.toString()}`);

    if (pluginHandle.isVideoMuted()){
        profile_picture.style.display = "none";
        self.innerHTML = '<i class = "fas fa-video"></i>';
        self.setAttribute('class','control_buttons');
        self.setAttribute('data-name','disable');
        video.style.visibility = 'visible';
        self.setAttribute('title','Mute your video');
        pluginHandle.unmuteVideo();
    }else {
        pluginHandle.muteVideo();
        self.innerHTML = '<i class = "fas fa-video-slash"></i>';
        self.setAttribute('class','inactive');
        self.setAttribute('data-name','enable');
        video.style.visibility = 'hidden';
        profile_picture.style.display = "block";
        self.setAttribute('title','Unmute your video');
    }
}

let handle_audio = async (self) => {
    var holder = document.getElementById(UID.toString());
    var microphone = document.getElementById(`name_${UID.toString()}`).firstElementChild;
    
    if (pluginHandle.isAudioMuted()){
        self.innerHTML = '<i class = "fas fa-microphone"></i>';
        self.setAttribute('class','control_buttons');
        self.setAttribute('data-name','mute');
        microphone.style.color = 'blue';
        microphone.setAttribute('class','fas fa-microphone');
        pluginHandle.unmuteAudio();
        self.setAttribute('title','Mute your microphone');

    }else {
        pluginHandle.muteAudio();
        self.innerHTML = '<i class = "fas fa-microphone-slash"></i>';
        self.setAttribute('class','inactive');
        self.setAttribute('data-name','unmute');
        microphone.style.color = 'red';
        microphone.setAttribute('class','fas fa-microphone-slash');
        self.setAttribute('title','Unmute your microphone');
    }
}

function add_comment(self){
    var input_box = self.parentElement.children[2];
    if (input_box.value.length > 0){
        var item = {'name':username,'message':input_box.value,
            'profile_picture':profile_picture,'id':UID};
        messagesocket.send(JSON.stringify(item));
        input_box.value = "";
    }
}

function add_comment_by_enter(keyboard_event){
    if (keyboard_event.keyCode == 13){
        var self = document.getElementById('livechat').lastElementChild.lastElementChild;
        add_comment(self);
    }
}

let screen_sharing = (self) => {
    /*AgoraRTC.createScreenVideoTrack({
        encoderConfig: '1080p_1',
        optimizationMode: 'details',
        screenSourceType: 'screen',
    }).then(localScreenTrack => {
        self.setAttribute('class','inactive');
        self.setAttribute('data-name','end');
        self.setAttribute('onclick',() => {
            client.unpublish(localScreenTrack);
        })
        messagesocket.send(JSON.stringify({'screen_sharing':true,'username':username,
                'profile_picture':profile_picture, 'id':UID}));
        localScreenTrack.on('track-ended', () => {
            client.unpublish(localScreenTrack);
            self.setAttribute('class','control_buttons');
            self.setAttribute('data-name','screen');
            self.setAttribute('onclick','screen_sharing(this)');

            var target_button = document.getElementById('controls').firstElementChild;

            if (target_button.dataset.name == 'enable') {
                client.publish(videoTrack);
            }
        })
    })*/


    pluginHandle.createOffer({
         tracks: [
               {type: 'audio', capture: true, recv: false},
               {type: 'video', capture: true, recv: false, remove: true},
               {type: 'screen', capture: true, recv: false}
            ],
         success: (jsep) => {
            let publish = { request: "configure", audio: true, screen: true };
            pluginHandle.send({ message: publish, jsep: jsep });
            messagesocket.send(JSON.stringify({'screen_sharing':true,'username':username,
                'profile_picture':profile_picture, 'id':UID}));
         },
         error: (error) => {
            console.log(error);
         }
      })

}

let open_classroom = (self) => {
    document.getElementById('meeting_info').style.display = "none";
    document.getElementById('whiteboard_container').style.display = "none";
    var tools = document.getElementById('meeting_tools');
    Array.from(tools.children).forEach((item) => {
        item.style.borderBottom = "none";
    })
    self.style.borderBottom = "2px solid rgba(0,0,200,0.6)";
}

function copy_link(self){
    self.innerHTML = '<i class = "fas fa-copy"></i>';
    var link = self.parentElement.firstElementChild.value;
    navigator.clipboard.writeText(link);
    send_notification('<i class = "fas fa-link"></i> Meeting invite link', 'successfully copied to clipboard');
    setTimeout(() => {
        self.innerHTML = '<i class = "far fa-copy"></i>';
    }, 2000)
}

function copy_passcode(self){
    self.innerHTML = '<i class = "fas fa-copy"></i>';
    var link = self.parentElement.firstElementChild.value;
    navigator.clipboard.writeText(link);
    send_notification('Meeting passcode', 'successfully copied to clipboard');
    setTimeout(() => {
        self.innerHTML = '<i class = "far fa-copy"></i>';
    }, 2000)
}

let open_whiteboard = (self) => {
    var tools = document.getElementById('meeting_tools');
    Array.from(tools.children).forEach((item) => {
        item.style.borderBottom = "none";
    })

    document.getElementById('meeting_info').style.display = "none";
    document.getElementById('whiteboard_container').style.display = "block";
    self.style.borderBottom = "2px solid rgba(0,0,200,0.6)";
}

let open_meet_info = (self) => {
    document.getElementById('whiteboard_container').style.display = "none";
    document.getElementById('meeting_info').style.display = "flex";
    var tools = document.getElementById('meeting_tools');
    Array.from(tools.children).forEach((item) => {
        item.style.borderBottom = "none";
    })
    self.style.borderBottom = "2px solid rgba(0,0,200,0.6)";
}

let full_screen = (self) => {
    self.requestFullscreen()
}

function open_chats(self){
    self.innerHTML = '<i class = "fas fa-comments"></i>'
    chats = true;
    document.getElementById('livechat').style.display = "block";
}

let raise_hand = (self) => {
    self.innerHTML = "<i class = 'fas fa-hand-paper'></i>";
    self.setAttribute('onclick','lower_hand(this)');
    self.setAttribute('data-name','unraise');
    messagesocket.send(JSON.stringify({'raise_hand':true,'username':username,'id':UID,'profile_picture':profile_picture}));
    self.setAttribute('title','Lower your hand');
}

let lower_hand = (self) => {
    self.innerHTML = "<i class = 'far fa-hand-paper'></i>";
    self.setAttribute('onclick','raise_hand(this)');
    self.setAttribute('data-name','raise');
    messagesocket.send(JSON.stringify({'lower_hand':true,'username':username,'id':UID}));
    self.setAttribute('title','Raise your hand');
}

function close_comments(){
    document.getElementById('livechat').style.display = "none";
    chats = false;
    document.getElementById('chats_button').innerHTML = '<i class = "far fa-comments"></i>'
}

function close_items(self){
    self.parentElement.parentElement.style.display = "none";
}

window.addEventListener('beforeunload',() => {
    leaveAndRemoveLocalStream();
});

let start_whiteboard = (room_token, room_uid) => {
    var whiteWebSdk = new WhiteWebSdk({
        appIdentifier: "kxGEgDNcEe2cCXezkLqgEg/Gf-OOdcaZPZ-pg",
        region: "us-sv",
      })
      
      var joinRoomParams = {
        uuid: room_uid,
        uid: UID.toString(),
        roomToken: room_token, 
      };
      
      whiteWebSdk.joinRoom(joinRoomParams).then(function(whiteboard_room) {
        whiteboard_room.bindHtmlElement(document.getElementById("whiteboard"));
        room = whiteboard_room;
        room.setWritable(true);

      }).catch(function(err) {
          console.error(err);
      });
 }
 
 let generate_room_token = (room_uid) => {
    fetch(`https://api.netless.link/v5/tokens/rooms/${room_uid}`,{
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'region':'us-sv',
            'token':'NETLESSSDK_YWs9UHI2SjR2T3RHUlBCai1fMSZub25jZT0yNTYwMTIzMC0zYjdjLTExZWQtODE5MC02ZDgwYzBkMGU1YmEmcm9sZT0wJnNpZz04NzdhZmY1YWE0YTUxYjczNjEzYTVlMjgzYmY3NDFhNTQyYTJiZTU5MjkyZGM2NTY4Yjg5NDJiMzYxNzBlMWY0'
        },
        body: JSON.stringify({'lifespan':3600000,"role":"admin"})
        }).then(response => {
        return response.json().then(data => {
            start_whiteboard(data, room_uid);
            fetch('/changeWhiteboardDetails/',{
                method: 'POST',
                headers:{
                    'Content-Type': 'application/json',
                    "X-CSRFToken": csrftoken,
                    'X-Requested-With':'XMLHttpRequest'
                },
                body: JSON.stringify({'room_token':data,'room_uuid':room_uid,'room_id':CHANNEL})
                })
            })
      })
  }

  let create_whiteboard_room = () => {
    fetch('https://api.netless.link/v5/rooms',{
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'region':'us-sv',
            'token':'NETLESSSDK_YWs9UHI2SjR2T3RHUlBCai1fMSZub25jZT0yNTYwMTIzMC0zYjdjLTExZWQtODE5MC02ZDgwYzBkMGU1YmEmcm9sZT0wJnNpZz04NzdhZmY1YWE0YTUxYjczNjEzYTVlMjgzYmY3NDFhNTQyYTJiZTU5MjkyZGM2NTY4Yjg5NDJiMzYxNzBlMWY0'
        },
        body: JSON.stringify({
          'isRecord': false
        })
        }).then(response => {
        return response.json().then(data => {
            generate_room_token(data.uuid);
        })
      })
  }

let getCredentials = () => {
    fetch(`/whiteboardDetails/?room_name=${CHANNEL}`,{
        method: 'GET'
    }).then((response) => {
        return response.json().then((data) => {
            start_whiteboard(data.room_token,data.room_uuid)
        })
    })
}

if (user_token == room_name) {
            create_whiteboard_room();
        }else {
            getCredentials();
        }

let clicker = (self) => {
    Array.from(document.getElementById('tools').children).forEach((item) => {
        item.style.backgroundColor = 'unset';
    })
    self.style.backgroundColor = "rgba(0, 0, 0, 0.17)";
    room.setMemberState(
        {currentApplianceName: 'clicker',
         shapeType: 'pentagram',
         strokeColor: [255,182,200],
         strokeWidth: 12,
         textSize: 40,});
}

let eraser = (self) => {
    Array.from(document.getElementById('tools').children).forEach((item) => {
        item.style.backgroundColor = 'unset';
    })
    self.style.backgroundColor = "rgba(0, 0, 0, 0.17)";
  room.setMemberState(
      {currentApplianceName: 'eraser',
       shapeType: 'pentagram',
       strokeColor: [255,182,200],
       strokeWidth: 12,
       textSize: 40,});
}

let text = (self) => {
    Array.from(document.getElementById('tools').children).forEach((item) => {
        item.style.backgroundColor = 'unset';
    })
    self.style.backgroundColor = "rgba(0, 0, 0, 0.17)";
  room.setMemberState(
    {currentApplianceName: 'text',
     shapeType: 'pentagram',
     strokeColor: [255,182,200],
     strokeWidth: 12,
     textSize: 40,});
}

var pen = (self) => {
    Array.from(document.getElementById('tools').children).forEach((item) => {
        item.style.backgroundColor = 'unset';
    })
    self.style.backgroundColor = "rgba(0, 0, 0, 0.17)";
  room.setMemberState(
      {currentApplianceName: 'pencil',
       shapeType: 'pentagram',
       strokeColor: [0,0,0],
       strokeWidth: 6,
       textSize: 40,});
}

let hand = (self) => {
    Array.from(document.getElementById('tools').children).forEach((item) => {
        item.style.backgroundColor = 'unset';
    })
    self.style.backgroundColor = "rgba(0, 0, 0, 0.17)";
    room.setMemberState(
      {currentApplianceName: 'hand',
       shapeType: 'pentagram',
       strokeColor: [255,182,200],
       strokeWidth: 12,
       textSize: 40,});
}

let clearBoard = () => {
    room.cleanCurrentScene();
}


let upload_image = () => {
    document.getElementById('photo').click();
}

localStorage.setItem('lastMeetingId',CHANNEL);










var localDescription;

const roomId = Number(document.getElementById('navbar').dataset.roomid);
var opaqueId = "meet-"+Janus.randomString(12);
var privateID = null;

Janus.init({
   debug: "all",
   callback: function () {
      console.log('initialized');
   }
})

var roomOptions = {
   request: 'create',
   room: roomId,
   publishers: 100,
   bitrate: 128000,
   bitrate_cap: true,
   notify_joining: true,
   record: false,
   description: 'video room',
}

var janus = new Janus({
   server: 'https://vschoolsmeet.tech:8089/janus',
   iceServers: [{urls:"stun:stun.l.google.com:19302"}],
   success: function () {
      setTimeout(start(), 6000);
   },
   error: function(error) {
      console.log(error);
   }
})

let start = () => {
    janus.attach({
        plugin: "janus.plugin.videoroom",
        opaqueId: opaqueId,
        success: (handle) => {
            pluginHandle = handle;
            handle.send({
                'message': { request: 'exists', 'room': roomId },
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
                        if (user_token == room_name) {
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
                                    }

                                }
                            })
                        }
                    }
                    messagesocket = new WebSocket(MessageSocket);
                    messagesocket.addEventListener('message',getSocketMessages);
            }
         })
      },

    iceState: (state) => {
        console.log('ICE state changed to', state);
    },

    mediaState: (medium, on, mid) => {
        console.log("Janus " + (on ? "started" : "stopped") + " receiving our " + medium + " (mid=" + mid + ")");
    },

    slowLink: (uplink, lost, mid) => {
        Janus.warn("Janus reports problems " + (uplink ? "sending" : "receiving") +
                              " packets on mid " + mid + " (" + lost + " lost packets)");
    },

    webrtcState: (on) => {
        console.log(`Peer connection state is ${(on ? "up" : "down")}  now`);
    },

    oncleanup: () => {
        Janus.log("Got a cleanup notification: we are unpublished now");
    },

    onlocaltrack: (track, added) => {
         // A local track to display has just been added (getUserMedia worked!) or removed
        localTracks.push(track);
        //track.enabled = false;
        localStream.addTrack(track);

        if (track.kind == 'audio') {
            audioTrack = track;
            
        }else if (track.kind == 'video') {
            videoTrack = track;
            
        }else {
            screenTrack = track;
        }
    },

    onremotetrack: (track, mid, added, metadata) => {
         // A remote track (working PeerConnection!) with a specific mid has just been added or removed
         // You can query metadata to get some more information on why track was added or removed
         // metadata fields:
         //   - reason: 'created' | 'ended' | 'mute' | 'unmute'
    },

    onmessage: (msg, jsep) => {
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
                        Janus.debug("Got publisher SDP!", jsep);
                        let publish = { request: "configure", audio: true, video: true };
                        pluginHandle.send({ message: publish, jsep: jsep });

                        var username = document.getElementById('main').dataset.username;
                        var profile_picture = document.getElementById('controls').dataset.profile_picture;
                        var user_token = document.getElementById('meeting_info').dataset.user_token;
                        var info = {'uid':UID,'profile_picture':profile_picture,'name':username,
                                'user_token':user_token, 'stream':localStream}
                        handleJoinedUser(info);
                    },
                    error: (error) => {
                        Janus.error("WebRTC error:", error);
                    }
                })

                if (msg['publishers']) {
                    var list = msg["publishers"];
                    list.forEach((item) => {
                        var id = item['id'];
                        var display = item['display'];
                        remoteFeed(display);
                  })
              }

            }else if (event === 'event') {
                console.log(msg);
                if (msg["joining"]) {
                    // A user has joined the video room
                }else if (msg["publishers"]) {
                    var list = msg["publishers"];
                    list.forEach((item) => {
                        var id = item['id'];
                        var display = item['display'];
                        remoteFeed(display);
                    })
                }else if (msg["leaving"]) {
                    // A user has left the video room
                    var user_id = msg["leaving"];
                    var holder = document.getElementById(user_id.toString());
                    holder.remove();
               }else if (msg['unpublished']) {
                  var user_id = msg["unpublished"];
               }
            }
         }

         if(jsep) {
            pluginHandle.handleRemoteJsep({ jsep: jsep });
         }
      },
      error: (error) => {
         console.log(error)
      }
   })
}

let remoteFeed = (display) => {
    var stream = new MediaStream();
    var info = JSON.parse(display);
    var handle;
    janus.attach({
        plugin: "janus.plugin.videoroom",
        opaqueId: opaqueId,
        success: (plugin) => {
            handle = plugin;

            let subscribe = {
               request: "join",
               room: roomId,
               ptype: "subscriber",
               feed: Number(info.id),
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
            console.log('ICE state changed to ',state);
        },

        webrtcState: (on) => {
            console.log(`Peer connection state is ${(on ? "up" : "down")} now`);
        },

        onremotetrack: (track, mid, added, metadata) => {
        // A remote track (working PeerConnection!) with a specific mid has just been added or removed
        // You can query metadata to get some more information on why track was added or removed
        // metadata fields:
        //   - reason: 'created' | 'ended' | 'mute' | 'unmute'
            console.log(`Track ${(added ? "added" : "removed")} Reason ${metadata.reason}`);
            var id = info.id;
            var mediaType = track.kind;

            if (added) {
                UserPublishedEvent(id, mediaType);
            }else {
                UserUnpublishedEvent(id, mediaType);
            }
        },

        onmessage: (msg, jsep) => {
            console.log(msg);
            if (jsep) {
                handle.createAnswer({
                    jsep: jsep,
                    tracks: [{type: 'data'}],

                    success: function(jsep) {
                        let body = { request: "start", room: roomId };
                        handle.send({ message: body, jsep: jsep });
                     },

                     error: function(error) {
                        Janus.error("WebRTC error:", error);
                     }
                })
            }
        },

        oncleanup: () => {
            Janus.log("Cleaned up feed, stopped receiving tracks from feed");
        },

        error: (error) => {
            Janus.error("WebRTC error:", error);
        }
    })
}