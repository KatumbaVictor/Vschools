if (navigator.mediaDevices.getDisplayMedia == undefined){document.getElementById('controls').children[3].remove()};
const UID = document.getElementById('container').dataset.id;
const username = document.getElementById('main').dataset.username;
const token = document.getElementById('main').dataset.token;
const profile_picture = document.getElementById('controls').dataset.profile_picture;
const APP_ID = '0eb3e08e01364927854ee79b9e513819';
const notifications = document.getElementById('notifications');
const container = document.getElementById('container');
const room_name = document.getElementById('controls').dataset.room_name;
const expression = /((ftp|http|https):\/\/)?(www\.)?([\w]+)(\.[\w]+)+(\/[\w]+)*/g;
var authorization = document.getElementById('controls').dataset.authorization;
var CHANNEL = window.location.pathname.split('/')[2];
var connection_protocol;
var all_hands = document.getElementById('all_hands');
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

var comment_holder = document.getElementById('livechat').children[1];
comment_holder.scrollTop = comment_holder.scrollHeight;


var file_types = ['audio/mpeg','audio/wav','application/pdf','image/jpeg','image/png','video/mp4',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];

var send_notification = (title, body) => {
    if (expression.test(body) == true) {
        body = body.replace(expression, (url) => {
            return `<a href = ${url} target="_blank">${url}</a>`;
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
}else {
    connection_protocol = 'ws';
}

let MessageSocket = `${connection_protocol}://${window.location.host}:8001/MessageSocket/${CHANNEL}/`;

var client = AgoraRTC.createClient({mode:'rtc',codec:'vp8'});

AgoraRTC.getCameras().then((devices) => {
    videoInputDevices = devices;
    if (videoInputDevices.length == 0) {
        var button = document.getElementById('controls').firstElementChild;
        button.innerHTML = '<i class = "fas fa-video-slash"></i>';
        button.setAttribute('class','inactive');
        button.setAttribute('data-name','enable');
    }
})

AgoraRTC.getMicrophones().then((devices) => {
    audioInputDevices = devices;
    if (audioInputDevices.length == 0) {
        var button = document.getElementById('controls').children[1];
        button.innerHTML = '<i class = "fas fa-microphone-slash"></i>';
        button.setAttribute('class','inactive');
        button.setAttribute('data-name','unmute');
    }
})

var videoInputDevices;
var audioInputDevices;

var videoTrack;
var audioTrack;

let createTracks = async () => {
    try {
        var tracks = await AgoraRTC.createMicrophoneAndCameraTracks();

        audioTrack = tracks[0];
        videoTrack = tracks[1];

        await videoTrack.setMuted(true);
        await audioTrack.setMuted(true);

        messagesocket = new WebSocket(MessageSocket);
        messagesocket.addEventListener('message',getSocketMessages);

        joinAndDisplayLocalStream();

    } catch (error) {
        var target_element = document.getElementById('container').firstElementChild;
        target_element.firstElementChild.remove();

        var child_one = document.createElement('i');
        child_one.setAttribute('class','fas fa-exclamation-triangle');
        target_element.prepend(child_one);

        target_element.lastElementChild.innerHTML = "Failed to start Camera and Microphone";
        
    }
}

createTracks();

let joinAndDisplayLocalStream = async () => {
    handleJoinedUser({'name':username,'uid':UID,'profile_picture':profile_picture,
        'user_token':user_token});

    client.on('user-joined', (user) => {
        fetch(`/getRoomMember/?room_id=${CHANNEL}&uid=${user.uid}`,{
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

    if (item.user_token == room_name) {
        document.getElementById('hosts').prepend(holder);
    }else {
        document.getElementById('hosts').appendChild(holder)
    }

    all_users = document.getElementById('hosts').children.length
    document.getElementById('meeting_tools').firstElementChild.innerHTML = `classroom (${all_users})`;

    holder.appendChild(name);
    holder.appendChild(profile_picture);
    holder.appendChild(hand);

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
        item.style.width = "270px";
        item.style.height = "270px";
    })

}

function view_users() {
    document.getElementById('meeting_tools').lastElementChild.click();
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

    all_users = document.getElementById('hosts').children.length
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

function countWords(str) {
    const arr = str.split(' ');
    return arr.filter(word => word !== '').length;
  }

function getImage() {
    document.getElementById('photo').click();
}

function sendFile(self) {
    if (self.files) {
        var form = new FormData();
        form.append("image",self.files[0]);
        form.append("uid",UID);
        form.append("fileType",self.files[0].type);
        form.append("fileName", self.files[0].name);

        var xhr = new XMLHttpRequest();

        /*xhr.upload.onloadstart = () => {
            document.getElementById('uploadProgress').style.display = "flex";
        }

        xhr.upload.onloadend = () => {
            document.getElementById('uploadProgress').style.display = "none";
        }

        var button = document.getElementById('progressContainer').lastElementChild;

        button.addEventListener('click', () => {
            xhr.abort();
            button.innerHTML = "Upload cancelled";
            setTimeout(() => {
                document.getElementById('uploadProgress').style.display = "none";
                button.innerHTML = "Cancel";
            },10000)
        })

        xhr.upload.onprogress = (event) => {
            var total = event.total;
            var loaded = event.loaded;

            var progressValue = (loaded / total) * 100;
            var progressElement = document.getElementById('progressElement').firstElementChild;
            progressElement.style.width = `${progressValue}%`;

            var percentage = document.getElementById('progressContainer').children[2];
            percentage.innerHTML = `${Math.trunc(progressValue)}%`;

        }*/

        xhr.onreadystatechange = () => {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                var data = JSON.parse(xhr.responseText);
                var fileUrl = data.fileUrl;
                var item = {'fileUrl':fileUrl,'profile_picture':profile_picture,
                    'id':UID,'name':username,'fileType':self.files[0].type,'fileName':self.files[0].name};
                messagesocket.send(JSON.stringify(item));
            }
        }

        if (file_types.includes(self.files[0].type)) {
            xhr.open('POST',window.location);
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            xhr.setRequestHeader('X-Requested-With','XMLHttpRequest');
            xhr.send(form);
        }else {
            post_message('<i class = "fas fa-exclamation-triangle"></i> Failed to send file');
        }
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
            return `<a href = ${url} target="_blank">${url}</a>`;
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

function add_comment_by_enter(keyboard_event){
    if (keyboard_event.keyCode == 13){
        var self = document.getElementById('livechat').lastElementChild.lastElementChild;
        add_comment(self);
    }
}

let screen_sharing = (self) => {
    AgoraRTC.createScreenVideoTrack({
        encoderConfig: '1080p_1',
        optimizationMode: 'details',
        screenSourceType: 'screen',
    }).then(localScreenTrack => {
        self.setAttribute('class','inactive');
        self.setAttribute('data-name','end');
        client.unpublish(videoTrack);
        client.publish(localScreenTrack);
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
    })
}

let start_recording = (resource_id) => {
    fetch(`https://api.agora.io/v1/apps/${APP_ID}/cloud_recording/resourceid/${resource_id}/mode/web/start`,{
        method: 'POST',
        headers:{
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization':'Basic ' + authorization
        },
        body: JSON.stringify({
            "cname": CHANNEL,
            "uid": UID.toString(),
            "clientRequest": {
                "token": token,
                "extensionServiceConfig": {
                    "errorHandlePolicy": "error_abort",
                    "extensionServices": [
                        {
                            "serviceName": "web_recorder_service",
                            "errorHandlePolicy": "error_abort",
                            "serviceParam": {
                                "url": `https://${window.location.host}/meeting_recording/${CHANNEL}`,
                                "audioProfile": 0,
                                "videoWidth": 1280,
                                "videoHeight": 720,
                                "maxRecordingHour": 1,
                                "maxVideoDuration": 200
                            }
                        }
                    ]
                },
                "recordingFileConfig": {
                    "avFileType": [
                        "hls",
                        "mp4"
                    ]
                },
                "storageConfig": {
                    "vendor": 1,
                    "region": 0,
                    "bucket": "vschools-file-bucket",
                    "accessKey": "AKIARLTR4RWUQPIM3AEB",
                    "secretKey": "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",
                    "fileNamePrefix": [
                        "media",
                    ]
                }
            }
        })
        }).then(response => {
        return response.json().then(data => {
            sid = data.sid;
            send_notification('Meeting recording', 'has started');
            recording = true;
            })
        })
}

let get_resource_id = (self) => {
    send_notification('Meeting recording', 'is still under development');
    /*
    self.innerHTML = '<i class = "fas fa-record-vinyl"></i> Stop recording';
    self.style.color = "rgba(255, 0, 0, 0.838)";
    self.setAttribute('onclick','stop_recording()');
    
    fetch(`/checkMeetingRecording/?room_id=${CHANNEL}`,{
            method: 'GET'
    }).then((response) => {
        return response.json().then(data => {
            if (data.MeetingRecording == false) {
                fetch(`https://api.agora.io/v1/apps/${APP_ID}/cloud_recording/acquire`,{
                method: 'POST',
                headers:{
                    'Content-Type': 'application/json;charset=utf-8',
                    'Authorization':'Basic ' + authorization
                },
                body: JSON.stringify({
                    'cname':CHANNEL,
                    'uid': UID.toString(),
                    "clientRequest": {
                        "region": "CN",
                        "resourceExpiredHour": 24,
                        "scene": 1}})
                }).then(response => {
                    return response.json().then(data => {
                        resource_id_value = data.resourceId;
                        start_recording(data.resourceId);})
                    })
            }else {
                send_notification('Dear user', 'this meeting is already being recorded you will find it in your recorded meetings');
            }
        })
    })
    */
}

let stop_recording = () => {
    fetch(`https://api.agora.io/v1/apps/${APP_ID}/cloud_recording/resourceid/${resource_id_value}/sid/${sid}/mode/web/stop`,{
        method: 'POST',
        headers:{
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization':'Basic ' + authorization
        },
        body: JSON.stringify({
          "cname": CHANNEL,
          "uid": UID.toString(),
          "clientRequest": {}
        })
        }).then(response => {
            recording = false;
            return response.json().then(data => {
                var mp4_file = `https://vschools-file-bucket.s3.amazonaws.com/media/${data.sid}_${CHANNEL}_0.mp4`;

                var form = new FormData();
                form.append("video_file_name",mp4_file);
        
                var xhr = new XMLHttpRequest();

                xhr.onreadystatechange = () => {
                if (xhr.readyState == XMLHttpRequest.DONE) {
                        console.log('meeting recorded successfully');
                    }
                }

                xhr.open('POST',window.location);
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
                xhr.setRequestHeader('X-Requested-With','XMLHttpRequest');
                xhr.send(form);
            })
        })
  }

let query_record_status = () => {
    fetch(`https://api.agora.io/v1/apps/${APP_ID}/cloud_recording/resourceid/${resource_id_value}/sid/${sid}/mode/web/query`,{
        method: 'GET',
        headers:{
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization':'Basic ' + authorization
        }
        }).then(response => {
        return response.json().then(data => {
            console.log(data);
        })
      })
}

let record_meeting = (self) => {
    get_resource_id();
    document.getElementById('options').style.display = "none";
    send_notification('Meeting recording', 'will start shortly');
  }

let end_recording = (self) => {
    stop_recording();
    self.innerHTML = '<i class = "fas fa-record-vinyl"></i> Record meeting';
    self.setAttribute('onclick','record_meeting(this)');
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

let captions = async (self) => {
    self.innerHTML = '<i class = "fas fa-closed-captioning"></i>';
    self.setAttribute('onclick','mute_captions(this)');
    post_message('<i class = "far fa-closed-captioning"></i> Auto generated subtitles have been turned on');
}

let mute_captions = async (self) => {
    self.innerHTML = '<i class = "far fa-closed-captioning"></i>';
    self.setAttribute('onclick','captions(this)');
    await connection.stopProcessing();
}

let show_hands = () => {
    document.getElementById('options').style.display = "none";
    document.getElementById('hands').style.display = "flex";
}

let show_qrcode = () => {
    document.getElementById('options').style.display = "none";
    document.getElementById('qrcode').style.display = "flex";
}

let raise_hand = (self) => {
    self.innerHTML = "<i class = 'fas fa-hand-paper'></i>";
    self.setAttribute('onclick','lower_hand(this)');
    self.setAttribute('data-name','unraise');
    messagesocket.send(JSON.stringify({'raise_hand':true,'username':username,'id':UID,'profile_picture':profile_picture}));
}

let lower_hand = (self) => {
    self.innerHTML = "<i class = 'far fa-hand-paper'></i>";
    self.setAttribute('onclick','raise_hand(this)');
    self.setAttribute('data-name','raise');
    messagesocket.send(JSON.stringify({'lower_hand':true,'username':username,'id':UID}));
}

function options(){
    document.getElementById('options').style.display = "flex";
}

function close_options(){
    document.getElementById('options').style.display = "none";
}

function get_link(self){
    document.getElementById('options').style.display = "none";
    document.getElementById('meeting_link').style.display = "flex";
}

function Cancel(self) {
    self.parentElement.parentElement.style.display = "none";
}

function close_comments(){
    document.getElementById('livechat').style.display = "none";
    chats = false;
}

let start_meeting = (self) => {
    self.style.display = "none";
    joinAndDisplayLocalStream();
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

console.log(user_token)
console.log(room_name)

if (user_token == room_name) {
            create_whiteboard_room();
        }else {
            getCredentials();
        }

let clicker = () => {
    room.setMemberState(
        {currentApplianceName: 'clicker',
         shapeType: 'pentagram',
         strokeColor: [255,182,200],
         strokeWidth: 12,
         textSize: 40,});
}

let eraser = () => {
  room.setMemberState(
      {currentApplianceName: 'eraser',
       shapeType: 'pentagram',
       strokeColor: [255,182,200],
       strokeWidth: 12,
       textSize: 40,});
}

let text = () => {
  room.setMemberState(
    {currentApplianceName: 'text',
     shapeType: 'pentagram',
     strokeColor: [255,182,200],
     strokeWidth: 12,
     textSize: 40,});
}

var pen = () => {
  room.setMemberState(
      {currentApplianceName: 'pencil',
       shapeType: 'pentagram',
       strokeColor: [0,0,0],
       strokeWidth: 6,
       textSize: 40,});
}

let hand = () => {
  room.setMemberState(
      {currentApplianceName: 'hand',
       shapeType: 'pentagram',
       strokeColor: [255,182,200],
       strokeWidth: 12,
       textSize: 40,});
}

let redo = () => {
  room.redo();
}

let undo = () => {
    room.undo()
}

let clearBoard = () => {
    room.cleanCurrentScene();
}


let upload_image = () => {
    document.getElementById('photo').click();
}