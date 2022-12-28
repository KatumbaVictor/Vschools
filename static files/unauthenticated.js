const UID = document.getElementById('container').dataset.id;
const username = document.getElementById('main').dataset.username;
var token;
const APP_ID = '0eb3e08e01364927854ee79b9e513819';
const notifications = document.getElementById('notifications');
const container = document.getElementById('container');
const room_name = document.getElementById('controls').dataset.room_name;
var authorization = document.getElementById('controls').dataset.authorization;
var CHANNEL = window.location.pathname.split('/')[2];
var connection_protocol;
var chats = false;
var set_captions = false;
var connection;
var resource_id_value;
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

fetch(`/get_token/?channel=${CHANNEL}`,{
    method: 'GET'
}).then(response => {
    return response.json().then(data => {
        token = response.token;
    })
})

var file_types = ['audio/mpeg','audio/wav','application/pdf','image/jpeg','image/png','video/mp4',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];

var send_notification = (title, body) => {
    var notification = document.getElementById('notification');
    var message = `<span>${title}</span> ${body}`;
    notification.innerHTML = message;
    notification.setAttribute('data-message',JSON.stringify(message));
    notification.style.display = "block";

    setTimeout(() => {
        notification.style.opacity = '1';
    }, 1300)

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
}else {
    connection_protocol = 'ws';
}

let meetingrecording = `${connection_protocol}://${window.location.host}/MeetingRecording/${CHANNEL}/`;
recording_socket = new WebSocket(meetingrecording);


let MessageSocket = `${connection_protocol}://${window.location.host}/MessageSocket/${CHANNEL}/`;

messagesocket = new WebSocket(MessageSocket);

var client = AgoraRTC.createClient({mode:'rtc',codec:'vp8'});

let joinAndDisplayLocalStream = async () => {
    client.on('user-joined', (user) => {
        fetch(`/getRoomMember/?room_id=${CHANNEL}$?uid=${user.uid}`,{
            method: 'GET'
        }).then((response) => {
            return response.json().then((data) => {
                handleJoinedUser(data);
            })
        })
    })
    client.on('user-published',UserPublishedEvent);

    await client.join(APP_ID, CHANNEL, token, UID);

    Array.from(document.getElementsByTagName('button')).forEach(item => {
        if (item.hasAttribute('disabled')){
            item.removeAttribute('disabled');
        }
    })
 
    client.on('token-privilege-will-expire',renew_client_token);
    client.on('token-privilege-did-expire',rejoin_session);
    client.on('user-left',handleUserLeft);
    client.on('user-unpublished',UserUnpublishedEvent);
}

joinAndDisplayLocalStream();

let UserUnpublishedEvent = async (user, mediaType) => {
    await client.unsubscribe(user, mediaType);
    var holder = document.getElementById(user.uid.toString());
    if (mediaType == 'video'){
        var profile_picture = document.getElementById(`profile_picture_${user.uid.toString()}`);
        profile_picture.style.display = "block";
    }else {
        var name = document.getElementById(`name_${user.uid.toString()}`);
        var microphone = name.firstElementChild;
        microphone.setAttribute('class','fas fa-microphone-slash');
        microphone.style.color = "red";
    }
}

let handleJoinedUser = (item) => {
    var name = document.createElement('p');
    name.setAttribute('id',`name_${item.uid.toString()}`);
    name.innerHTML = `<i class = 'fas fa-microphone-slash'></i> ${item.name} <span></span>`;

    var profile_picture = document.createElement('img');
    profile_picture.setAttribute('id',`profile_picture_${item.uid.toString()}`);
    profile_picture.setAttribute('src',item.profile_picture);

    var holder = document.createElement('div');
    holder.setAttribute('id',item.uid.toString());
    holder.setAttribute('class','holder');
    holder.setAttribute('ondblclick','full_screen(this)');
    document.getElementById('hosts').prepend(holder);

    all_users += 1
    document.getElementById('meeting_tools').firstElementChild.innerHTML = `classroom (${all_users})`;

    holder.appendChild(name);
    holder.appendChild(profile_picture);

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

    Array.from(document.getElementsByClassName('holder')).forEach((item) => {
        item.style.width = "260px";
        item.style.height = "260px";
    })

}


let UserPublishedEvent = async (user, mediaType) => {
    await client.subscribe(user, mediaType);
    var holder = document.getElementById(user.uid.toString());

    if (holder == null) {
        setTimeout(UserPublishedEvent(user, mediaType), 2000);
    }else {
        if (mediaType === 'video'){
            user.videoTrack.play(holder);
            var player = holder.lastElementChild;
            var video = holder.lastElementChild.firstElementChild;
            var image = document.getElementById(`profile_picture_${user.uid.toString()}`);
            image.style.display = "none";
            
            player.style.display = "flex";
            player.style.flexDirection = "column";
            player.style.alignItems = "center";
            player.style.justifyItems = "center";

            video.setAttribute('style','height: 100%; width: auto; max-width: 100%;'); 
        }

        if (mediaType === 'audio'){
            user.audioTrack.play();
            var name = document.getElementById(`name_${user.uid.toString()}`);
            var microphone = name.firstElementChild;
            microphone.setAttribute('class','fas fa-microphone');
            microphone.style.color = "blue";
        }
    }
}

let handleUserLeft = async (user) => {
    document.getElementById(user.uid.toString()).remove();
    document.getElementById(`participant_${user.uid.toString()}`).remove();

    all_users -= 1
    document.getElementById('meeting_tools').firstElementChild.innerHTML = `classroom (${all_users})`;
}

let leaveAndRemoveLocalStream = async () => {
    messagesocket.close();
    videoTrack.stop();
    audioTrack.stop();
    videoTrack.close();
    audioTrack.close()
    client.leave();

    if (recording == true) {
        stop_recording();
    }

    window.open('/','_self');
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

let getSocketMessages = function(self){
    var response = JSON.parse(self.data);
    var comment_holder = document.getElementById('livechat').children[1];

    if (response.message) {
        var container = document.createElement('div');
        
        var time = getCurrentTime();
        var container = `
            <div class = "message_container">
                <img class = 'profile_picture' src = "${response.profile_picture}"/>
                <p class = "user_name">${response.name} <span>${time}</span></p>
                <p class = "message">${response.message}</p>
            </div>
        `
        comment_holder.innerHTML += container;
        comment_holder.scrollTop = comment_holder.scrollHeight;

        if (chats === false) {
            send_notification(response.name, response.message);
        }
    }else if (response.raise_hand) {
        send_notification(`<i class = "fas fa-hand-paper"></i> ${response.username}`,'is raising a hand');

        var item = document.createElement('i');
        item.setAttribute('class','fas fa-hand');
    }else if (response.screen_sharing) {
        send_notification(response.username, 'is sharing screen');
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

messagesocket.addEventListener('message',getSocketMessages);


let handle_camera = async (self) => {
    var holder = document.getElementById(UID.toString());
    var profile_picture = document.getElementById(`profile_picture_${UID.toString()}`);
    var video = holder.lastElementChild.firstElementChild;
    if (videoInputDevices.length > 0) {
        if (videoTrack.muted){
            profile_picture.style.display = "none";
            self.innerHTML = '<i class = "fas fa-video"></i>';
            self.setAttribute('class','control_buttons');
            self.setAttribute('data-name','disable');

            if (video_track_playing == false) {
                videoTrack.play(holder);
                video_track_playing == true;
                client.publish(videoTrack);
                /*video.setAttribute('style','height: 100%; width: auto; max-width: 100%;');*/
            }

            await videoTrack.setMuted(false);

            var item = holder.children[2];
            item.style.backgroundColor = "white";

        }else {
            await videoTrack.setMuted(true);
            self.innerHTML = '<i class = "fas fa-video-slash"></i>';
            self.setAttribute('class','inactive');
            self.setAttribute('data-name','enable');
            profile_picture.style.display = "block";
            video.style.display = "block";
        }
    }else {
        post_message('You have no webcam attached to your device');
    }
}

let handle_audio = async (self) => {
    var holder = document.getElementById(UID.toString());
    var microphone = document.getElementById(`name_${UID.toString()}`).firstElementChild;
    
    if (audioInputDevices.length > 0) {
        if (audioTrack.muted){
            await audioTrack.setMuted(false);
            self.innerHTML = '<i class = "fas fa-microphone"></i>';
            self.setAttribute('class','control_buttons');
            self.setAttribute('data-name','mute');
            microphone.style.color = 'blue';
            microphone.setAttribute('class','fas fa-microphone');

            if (audio_track_playing == false) {
                audio_track_playing == true;
                client.publish(audioTrack);
            }
        }else {
            await audioTrack.setMuted(true);
            self.innerHTML = '<i class = "fas fa-microphone-slash"></i>';
            self.setAttribute('class','inactive');
            self.setAttribute('data-name','unmute');
            microphone.style.color = 'red';
            microphone.setAttribute('class','fas fa-microphone-slash');
        }
    }else {
        post_message('You have no audio input device attached');
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

let renew_client_token = () => {
    fetch(`/get_token/?channel=${CHANNEL}`,{
        method: 'GET'
    }).then(response => {
        return response.json().then(data => {
            client.renewToken(data.token);
        })
    })
}

let rejoin_session = () => {
    fetch(`/get_token/?channel=${CHANNEL}`,{
        method: 'GET'
    }).then(response => {
        return response.json().then(data => {
            client.join(APP_ID, CHANNEL, data.token);
        })
    })
}

let full_screen = (self) => {
    self.requestFullscreen()
}

let search_user = (self) => {
    var input_value = self.value.toUpperCase();
    var parent = Array.from(document.getElementsByClassName('user_holder'))[0];
    Array.from(parent.children).forEach((item) => {
        if (!item.hasAttribute('class')) {
            if (!item.innerHTML.includes(input_value)) {
                item.style.visibility = "hidden";
            }else {
                item.style.visibility = "unset";
            }
        }
    })
}

function open_chats(){
    chats = true;
    document.getElementById('livechat').style.display = "block";
}

let show_hands = () => {
    document.getElementById('options').style.display = "none";
    document.getElementById('hands').style.display = "flex";
}

function Cancel(self) {
    self.parentElement.parentElement.style.display = "none";
}

function close_comments(){
    document.getElementById('livechat').style.display = "none";
    chats = false;
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
                    "X-CSRFToken": getCookie('csrftoken'),
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


getCredentials();

let upload_image = () => {
    document.getElementById('photo').click();
}