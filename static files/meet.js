if (navigator.mediaDevices.getDisplayMedia == undefined){controls.children[3].remove();};
const my_id = document.getElementById('controls').dataset.id;
const username = document.getElementById('main').dataset.username;
const user_token = document.getElementById('main').dataset.channel;
var notifications = document.getElementById('notifications');
var container = document.getElementById('container');
const APP_ID = '0eb3e08e01364927854ee79b9e513819';
var CHANNEL = document.getElementById('container').dataset.token;
var token = document.getElementById('meeting_link').dataset.token;
var UID = Number(document.getElementById('controls').dataset.id);
var connection_protocol;
var profile_picture = document.getElementById('controls').dataset.profile_picture;
let role = document.getElementById('comments').dataset.role;
var all_hands = document.getElementById('all_hands');
var chats = false;
var set_captions = false;
var connection;

(async () => {
    try {
        const symbl = new Symbl({
            appId: '6f77634b73416c4c616b575949676d576e494b4a304c44564e446e34644b7551',
            appSecret: '715341643953573431314d65344935496a716a7157566b5078513532445234757a52726a31364a69766f6c4745624430703237525f5637314435356a3774376e',
            reconnectOnError: true
        });
        connection = await symbl.createConnection();

        connection.on("speech_recognition", (speechData) => {
            const { punctuated } = speechData;
            socket.send(JSON.stringify({'caption':punctuated.transcript,'id':UID.toString()}));
        });
        
    } catch(e) {
        
    }
  })();

var qr_code_holder = document.getElementById('qrcode');
qr_code_holder.firstElementChild.setAttribute('autofocus','');
var qr_code = new QRCode(document.getElementById('qrcode').firstElementChild,{
    text: document.getElementById('meeting_link').firstElementChild.children[2].value,
    width: 128,
    height: 128
});

qr_code_holder.addEventListener('mousedown',() => {
    qr_code_holder.style.display = "none";
})

document.getElementById('options').addEventListener('mouseup',() => {
    document.getElementById('options').style.display = "none";
})

var element = Array.from(document.getElementsByClassName('hands_button'))[0];
element.style.setProperty('--raised_hands','none');

if (window.location.protocol == 'https:'){
    connection_protocol = 'wss';
}else {
    connection_protocol = 'ws';
}

let websocket_url = `${connection_protocol}://${window.location.host}/meet/${CHANNEL}/${UID}/${role}/`;
var socket = new WebSocket(websocket_url);
var client = AgoraRTC.createClient({mode:'rtc',codec:'vp8'});
var remoteUsers = [];
var localTracks = [];

client.on('user-joined',(user) => {
    localTracks.forEach((item) => {
        client.publish(item);
    })
})

let joinAndDisplayLocalStream = async () => {
    client.on('user-published',handleNewUser);

    await client.join(APP_ID, CHANNEL, token, UID);

    localTracks = await AgoraRTC.createMicrophoneAndCameraTracks();

    Array.from(document.getElementsByTagName('button')).forEach(item => {
        if (item.hasAttribute('disabled')){
            item.removeAttribute('disabled');
        }
    })
    
    var name = document.createElement('p');
    name.setAttribute('id',`name_${UID.toString()}`);
    name.innerHTML = `<i class = 'fas fa-microphone'></i> ${username} <span></span>`;
    name.firstElementChild.style.color = 'blue';

    var image = document.createElement('img');
    image.setAttribute('src',document.getElementById('controls').dataset.profile_picture);
    image.setAttribute('id',`profile_picture_${UID.toString()}`);

    var holder = document.createElement('div');
    holder.setAttribute('id',UID.toString());
    holder.setAttribute('class','holder');

    var loader = container.firstElementChild;

    if (loader.getAttribute('class') == "loader_holder"){
        loader.remove();
    }

    container.appendChild(holder);

    container.style.alignContent = "unset";
    container.style.justifyContent = "unset";

    holder.appendChild(name);
    holder.appendChild(image);

    localTracks[1].play(holder);
    image.style.display = "none";

    if (Array.from(document.getElementsByClassName('holder')).length > 1) {
        container.style.gridTemplateColumns = "repeat(auto-fit, minmax(300px, 1fr))";
        container.style.gridAutoRows = "300px";
    }
    
    var player = holder.lastElementChild;
    var video = holder.lastElementChild.firstElementChild;
    player.style.display = "flex";
    player.style.flexDirection = "column";
    player.style.alignItems = "center";
    player.style.justifyItems = "center";

    video.setAttribute('style','height: 100%; width: auto; max-width: 100%;');

    client.on('token-privilege-will-expire',renew_client_token);
    client.on('token-privilege-did-expire',rejoin_session);
    client.on('user-left',handleUserLeft);
    client.on('user-unpublished',UserUnpublishedEvent);

    await client.publish([localTracks[0],localTracks[1]]);
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
    name.innerHTML = `<i class = 'fas fa-microphone-slash'></i> ${item.name} <span></span>`;

    var profile_picture = document.createElement('img');
    profile_picture.setAttribute('id',`profile_picture_${item.uid.toString()}`);
    profile_picture.setAttribute('src',item.profile_picture);

    container.style.gridTemplateColumns = "repeat(auto-fit, minmax(300px, 1fr))";
    container.style.gridAutoRows = "300px";

    var holder = document.createElement('div');
    holder.setAttribute('id',item.uid.toString());
    holder.setAttribute('class','holder');
    container.appendChild(holder);

    holder.appendChild(name);
    holder.appendChild(profile_picture);

    var loader = container.firstElementChild;

    if (loader.getAttribute('class') == "loader_holder"){
        loader.remove();
    }

    var player = holder.lastElementChild;
    
    player.style.display = "flex";
    player.style.flexDirection = "column";
    player.style.alignItems = "center";
    player.style.justifyItems = "center";
    
    var parent = Array.from(document.getElementsByClassName('user_holder'))[0];

    var new_user = document.createElement('p');
    new_user.setAttribute('id',`participant_${item.uid.toString()}`);
    new_user.innerHTML = `<img src = '${item.profile_picture}'/>${item.name}`;
    parent.appendChild(new_user);

    var button  = document.getElementById('controls').children[2];
    button.setAttribute('data-description',parent.children.length - 1);
}

let handleNewUser = async (user, mediaType) => {
    await client.subscribe(user, mediaType);
    var holder = document.getElementById(user.uid.toString());
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

let handleUserLeft = async (user) => {
    document.getElementById(user.uid.toString()).remove();

    if (Array.from(document.getElementsByClassName('holder')).length == 1){
        container.style.gridTemplateColumns = "auto";
        container.style.gridAutoRows = "auto";
    }

    document.getElementById(`participant_${user.uid.toString()}`).remove();

    var parent = Array.from(document.getElementsByClassName('user_holder'))[0];

    var target_button = document.getElementById('controls').children[2];
    target_button.setAttribute('data-description',parent.children.length - 1);
}

let leaveAndRemoveLocalStream = async () => {
    socket.close();
    localTracks.forEach(item => {
        item.stop();
        item.close();
    }) 
    client.leave();
    window.open('/','_self');
}

function countWords(str) {
    const arr = str.split(' ');
    return arr.filter(word => word !== '').length;
  }

let getSocketMessages = function(self){
    var response = JSON.parse(self.data);
    var comment_holder = document.getElementById('comments').children[2];

    if(response.message){
        var container = document.createElement('div');
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
        var container = `
            <div>
                <img src = "${response.profile_picture}"/>
                <p class = "user_name">${response.name} <span>${time}</span></p>
                <p class = "message">${response.message}</p>
            </div>
        `
        comment_holder.innerHTML += container;
        comment_holder.scrollTop = comment_holder.scrollHeight;

        if (chats === false) {
            var text = document.createElement('p');
            text.innerHTML = `<span>${response.name}</span> ${response.message}`;
            notifications.appendChild(text);
            notifications.scrollTop = notifications.scrollHeight;
            setTimeout(() => {text.style.opacity = "0"}, 5000);
        }
    }else if (response.raise_hand) {
        var element = Array.from(document.getElementsByClassName('hands_button'))[0];
        element.style.setProperty('--raised_hands','block');

        var text = document.createElement('p');
        text.innerHTML = `<i class = "fas fa-hand-paper"></i> ${response.username}`;
        notifications.appendChild(text);
        notifications.scrollTop = notifications.scrollHeight;
        setTimeout(() => {text.style.opacity = "0"}, 5000);

        all_hands.innerHTML = response.hands;

        var parent = document.getElementById('hands');
        var child  = document.createElement('div');
        child.setAttribute('id',`hand_${response.id.toString()}`);
        child.innerHTML = `
            <i class = "fas fa-hand-paper"></i>
            <p>${response.username}</p>
        `
        parent.prepend(child);
    }else if (response.caption) {
        var parent = document.getElementById(`name_${response.id.toString()}`).lastElementChild;
        if (countWords(parent.innerHTML) > 12) {
            parent.innerHTML = '';
        }
        parent.innerHTML += ` ${response.caption}`;
    }else if (response.lower_hand) {
        all_hands.innerHTML = response.hands;
        if (document.getElementById('hands').children.length == 0) {
            element.style.setProperty('--raised_hands','none');
        }
    }else if (response.screen_sharing) {
        var text = document.createElement('p');
        text.innerHTML = `<i class = "fas fa-laptop"></i> ${response.username} is sharing screen`;
        notifications.appendChild(text);
        notifications.scrollTop = notifications.scrollHeight;
        setTimeout(() => {text.style.opacity = "0"}, 5000);
    }else if (response.user_joined) {
        if (response.uid.toString() != UID.toString()) {
            if (document.getElementById(response.uid.toString()) == null) {
                remoteUsers.push(response);
                handleJoinedUser(response);
            }
        }
    }
}

socket.addEventListener('message',getSocketMessages);

let handle_camera = async (self) => {
    var profile_picture = document.getElementById(`profile_picture_${UID.toString()}`);
    if (localTracks[1].muted){
        profile_picture.style.display = "none";
        await localTracks[1].setMuted(false);
        self.innerHTML = '<i class = "fas fa-video"></i>';
        self.setAttribute('class','control_buttons');
        self.setAttribute('data-description','disable');

        var text = document.createElement('p');
        text.innerHTML = '<i class = "fas fa-video"></i> Your camera is enabled';
        notifications.appendChild(text);
        notifications.scrollTop = notifications.scrollHeight;
        setTimeout(() => {text.style.opacity = "0"}, 5000);
    }else {
        await localTracks[1].setMuted(true);
        self.innerHTML = '<i class = "fas fa-video-slash"></i>';
        self.setAttribute('class','inactive');
        self.setAttribute('data-description','enable');
        profile_picture.style.display = "block";
    }
}

let handle_audio = async (self) => {
    var holder = document.getElementById(my_id.toString());
    var microphone = document.getElementById(`name_${UID.toString()}`).firstElementChild;
    
    if (localTracks[0].muted){
        await localTracks[0].setMuted(false);
        self.innerHTML = '<i class = "fas fa-microphone"></i>';
        self.setAttribute('class','control_buttons');
        self.setAttribute('data-description','mute');
        microphone.style.color = 'blue';
        microphone.setAttribute('class','fas fa-microphone');

        var text = document.createElement('p');
        text.innerHTML = '<i class = "fas fa-microphone"></i> Your microphone is unmuted';
        notifications.appendChild(text);
        notifications.scrollTop = notifications.scrollHeight;
        setTimeout(() => {text.style.opacity = "0"}, 5000);
    }else {
        await localTracks[0].setMuted(true);
        self.innerHTML = '<i class = "fas fa-microphone-slash"></i>';
        self.setAttribute('class','inactive');
        self.setAttribute('data-description','unmute');
        microphone.style.color = 'red';
        microphone.setAttribute('class','fas fa-microphone-slash');
    }
}

let screen_sharing = (self) => {
    AgoraRTC.createScreenVideoTrack({
        encoderConfig: '1080p_1',
        optimizationMode: 'details',
        screenSourceType: 'screen',
    }).then(localScreenTrack => {
        self.setAttribute('class','inactive');
        self.setAttribute('data-description','end');
        client.unpublish(localTracks[1]);
        client.publish(localScreenTrack);

        socket.send(JSON.stringify({'screen_sharing':true,'username':username}));

        localScreenTrack.on('track-ended', () => {
            client.unpublish(localScreenTrack);
            client.publish(localTracks[1]);
            self.setAttribute('class','control_buttons');
            self.setAttribute('data-description','screen');
        })
    })
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
    var options = document.getElementById('options');
    var main = document.getElementById('main');
    var comments = document.getElementById('comments').parentElement;
    var grid_value = window.getComputedStyle(main).getPropertyValue('grid-template-columns');
    var display_value = window.getComputedStyle(comments).getPropertyValue('display');

    options.style.display = "none";

    if (display_value == 'flex'){
        comments.style.display = 'none';
        self.innerHTML = "<i class = 'far fa-comments'></i>";
        if (grid_value != 'auto'){
            main.style.gridTemplateColumns = 'auto';
        }
        chats = false
    }else {
        var button = document.getElementById('comments').firstElementChild;
        var button_display = window.getComputedStyle(button).getPropertyValue('visibility');
        
            main.style.gridTemplateColumns = 'auto 340px';
        
        comments.style.display = 'flex';
        chats = true;
    }
}

let captions = async (self) => {
    self.innerHTML = '<i class = "fas fa-closed-captioning"></i>';
    self.setAttribute('onclick','mute_captions(this)');
    var text = document.createElement('p');
    text.innerHTML = 'Subtitles have been turned on';
    notifications.appendChild(text);
    notifications.scrollTop = notifications.scrollHeight;
    setTimeout(() => {text.style.opacity = "0"}, 5000);
    await connection.startProcessing({
        insightTypes: ["question", "action_item", "follow_up"],
        config: {
          encoding: "OPUS"
        },
        speaker: {
          userId: 'user_email',
          name: username
        }
      });
}

let mute_captions = async (self) => {
    self.innerHTML = '<i class = "far fa-closed-captioning"></i>';
    self.setAttribute('onclick','captions(this)');
    await connection.stopProcessing();
}

let show_hands = () => {
    document.getElementById('options').style.display = "none";
    document.getElementById('hands').style.display = "grid";
}

let show_qrcode = () => {
    document.getElementById('options').style.display = "none";
    document.getElementById('qrcode').style.display = "flex";
}

let raise_hand = (self) => {
    self.innerHTML = "<i class = 'fas fa-hand-paper'></i>";
    self.setAttribute('onclick','lower_hand(this)');
    socket.send(JSON.stringify({'raise_hand':true,'username':username,'id':UID}));
}

let lower_hand = (self) => {
    self.innerHTML = "<i class = 'far fa-hand-paper'></i>";
    self.setAttribute('onclick','raise_hand(this)');
    socket.send(JSON.stringify({'lower_hand':true,'username':username,'id':UID}));
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

function close_comments(self){
    self.parentElement.parentElement.style.display = 'none';
    var main = document.getElementById('main');
    main.style.gridTemplateColumns = "auto";
    chats = false;
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

function add_comment(self){
    var input_box = self.parentElement.firstElementChild;
    if (input_box.value.length > 0){
        var item = {'name':username,'message':input_box.value,
            'profile_picture':profile_picture,'id':my_id};
        socket.send(JSON.stringify(item));
        input_box.value = "";
    }
}

function add_comment_by_enter(keyboard_event){
    if (keyboard_event.keyCode == 13){
        var self = document.getElementById('comments').lastElementChild.lastElementChild;
        add_comment(self);
    }
}

let start_meeting = (self) => {
    self.style.display = "none";
    joinAndDisplayLocalStream();
}

function close_items(self){
    document.getElementById('viewers').style.display = 'none';
}

function get_views(){
    document.getElementById('viewers').style.display = "flex";
}

function copy_link(self){
    var parent = self.parentElement.parentElement;
    var link = self.parentElement.children[2].value;
    navigator.clipboard.writeText(link);
    self.innerHTML = "<i class = 'fas fa-copy'></i> link copied";
    setTimeout(() => {
        parent.style.display = "none";
        self.innerHTML = "<i class = 'far fa-copy'></i> Copy link";
    },800)
}

window.addEventListener('beforeunload',() => {
    socket.close();
    localTracks.forEach(item => {
        item.stop();
        item.close();
    }) 
    client.leave();
});

joinAndDisplayLocalStream();