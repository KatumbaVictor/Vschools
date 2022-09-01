const APP_ID = '0eb3e08e01364927854ee79b9e513819';
const role = 'host';
const CHANNEL = document.getElementById('comments').dataset.usertoken;
var UID = Number(document.getElementById('main').dataset.id);
const username = document.getElementById('main').dataset.username;
var container = document.getElementById('container');
var token;
var connection_protocol;
var session_title;
var session_description;

if (window.location.protocol === 'https:'){
    connection_protocol = 'wss';
}else {
    connection_protocol = 'ws';
}

var screen_track;

var socket;

fetch(`/get_token/?channel=${CHANNEL}`,{
    method: 'GET'
}).then(response => {
    return response.json().then(data => {
        token = data.token;
    })
})

const SpeechRecognition = window.SpeechRecognition || webkitSpeechRecognition;
const SpeechRecognitionEvent = window.SpeechRecognitionEvent || webkitSpeechRecognitionEvent;
const recognition = new SpeechRecognition();
var content = '';
recognition.continuous = true;
recognition.interimResults = true;
recognition.lang = 'en-US';

recognition.onresult = (event) => {
    var current = event.resultIndex;
    var transcript = event.results[current][0].transcript;
    content += transcript;
    socket.send(JSON.stringify({'caption':content}));
}

var client = AgoraRTC.createClient({mode:'live',codec:'vp8'});
client.setClientRole('host');
var localTracks = [];
var remoteUsers = {};
var profile_picture = document.getElementById('controls').dataset.profile_picture;

let joinAndDisplayLocalStream = async () => {
    await client.join(APP_ID, CHANNEL, token, UID);
    localTracks = await AgoraRTC.createMicrophoneAndCameraTracks();
    container.removeChild(container.children[2]);

    var holder = document.createElement('div');
    container.appendChild(holder);
    
    Array.from(document.getElementsByTagName('button')).forEach(item => {
        if (item.hasAttribute('disabled')){
            item.removeAttribute('disabled');
        }
    })
    localTracks[1].play(holder);
    
    var local_video_track = localTracks[1].getMediaStreamTrack();
    local_video_track.addEventListener('mute',() => {
        var image = document.getElementById('image_container');
        image.style.display = "flex";
    })
    
    var video = document.getElementsByTagName('video')[0];
    video.removeAttribute('style');
    var player = video.parentElement;
    player.setAttribute('style','width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;');
    await client.publish([localTracks[0],localTracks[1]]);
    client.on('user-published',handleNewUser);
    client.on('user-left',handleUserLeft);
}

let getSocketMessages = function(self){
    var response = JSON.parse(self.data);
    if (response.message){
        var message = response.message;
        var comment_holder = document.getElementById('comments').children[2];
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
    }
}

let handleNewUser = async (user, mediaType) => {
    fetch (`/getMember/?uid=${user.uid}&room_name=${CHANNEL}`,{
        method: "GET",
        headers: { 'Accept': 'application/json',
                'X-Requested-With':'XMLHttpRequest'},
    }).then(response => {
        return response.json().then(item => {
            /*var container = document.getElementById('viewers').firstElementChild.children[2];
            var name = document.createElement('p');
            name.setAttribute('uid',user.uid);
            name.innerHTML = `<img src = '${response.profile_picture}'/>${item.name}`;
            container.prepend(name);
            var target_button = document.getElementById('controls').children[2];
            target_button.setAttribute('data-description',container.children.length);*/
            var container = document.getElementById('container');
            
            if (response.role == 'co_host'){
                if (mediaType == 'video'){
                    if (document.getElementById(user.uid) == null){
                        var holder = document.createElement('div');
                        holder.setAttribute('id',user.uid);
                        container.appendChild(holder);
                        user.videoTrack.play(holder);
                    }
                }
                if (mediaType == 'audio'){
                    user.audioTrack.play();
                }
            }
        })
    })
}

let handleUserLeft = async (user) => {
    var parent = document.getElementById('viewers').firstElementChild.children[2];
    parent.forEach(item => {
        if (item.dataset.uid == user.uid){
            parent.removeChild(item);
        }
    })
    var target_button = document.getElementById('controls').children[2];
    target_button.setAttribute('data-description',container.children.length);
}

let screen_sharing = (self) => {
    AgoraRTC.createScreenVideoTrack({
        encoderConfig: '1080p_1',
        optimizationMode: 'details',
        screenSourceType: 'screen',
    }).then(localScreenTrack => {
        localTracks[1].setMuted(true);
        client.unpublish(localTracks[1]);
        client.publish(localScreenTrack);
        screen_track = localScreenTrack;
        var image = document.getElementById('image_container');
        image.style.display = "flex";
        image.children[1].innerHTML = "You're sharing your screen";
        self.setAttribute('data-description','close');
        self.setAttribute('onclick','close_screen_sharing(this)');
        localScreenTrack.on('track-ended',() => {
            image.style.display = "none";
            client.unpublish(localScreenTrack);
            localTracks[1].setMuted(false);
            client.publish(localTracks[1]);
            image.children[1].innerHTML = "Video muted";
            self.setAttribute('data-description','screen');
            self.setAttribute('onclick','screen_sharing(this)');
        })
    })
}

let close_screen_sharing = (self) => {
    var image = document.getElementById('image_container');
    image.style.display = "none";
    image.children[1].innerHTML = "Video muted";
    client.unpublish(screen_track);
    client.publish(localTracks[1]);
    self.setAttribute('data-description','screen');
    self.setAttribute('onclick','screen_sharing(this)');
}

function add_comment(self){
    var input_box = self.parentElement.firstElementChild;
    if (input_box.value.length > 0){
        var item = {'name':username,'message':input_box.value,'profile_picture':profile_picture};
        socket.send(JSON.stringify(item));
        input_box.value = "";
    }
}

let handle_camera = async (self) => {
    if (localTracks[1].muted){
        await localTracks[1].setMuted(false);
        self.innerHTML = '<i class = "fas fa-video"></i>';
        self.setAttribute('class','control_buttons');
        self.setAttribute('data-description','disable');
    }else {
        await localTracks[1].setMuted(true);
        self.innerHTML = '<i class = "fas fa-video-slash"></i>';
        self.setAttribute('class','inactive');
        self.setAttribute('data-description','enable');
    }
}

let handle_audio = async (self) => {
    if (localTracks[0].muted){
        await localTracks[0].setMuted(false);
        self.innerHTML = '<i class = "fas fa-microphone"></i>';
        self.setAttribute('class','control_buttons');
        self.setAttribute('data-description','mute');
    }else {
        await localTracks[0].setMuted(true);
        self.innerHTML = '<i class = "fas fa-microphone-slash"></i>';
        self.setAttribute('class','inactive');
        self.setAttribute('data-description','unmute');
    }
}

function get_views(self){
    document.getElementById('viewers').style.display = "flex";
}

function toggle_chat(self){
    var main = document.getElementById('main');
    var comments = document.getElementById('comments').parentElement;
    var grid_value = window.getComputedStyle(main).getPropertyValue('grid-template-columns');
    var display_value = window.getComputedStyle(comments).getPropertyValue('display');

    if (display_value == 'flex'){
        comments.style.display = 'none';
        self.innerHTML = "<i class = 'far fa-comments'></i>";
        if (grid_value != 'auto'){
            main.style.gridTemplateColumns = 'auto';
        }
        self.setAttribute('data-description','hide');
    }else {
        var button = document.getElementById('comments').firstElementChild;
        var button_display = window.getComputedStyle(button).getPropertyValue('visibility');
        if (button_display == 'hidden'){
            main.style.gridTemplateColumns = 'auto 340px';
        }
        comments.style.display = 'flex';
        self.innerHTML = "<i class = 'fas fa-comments'></i>";
        self.setAttribute('data-description','show');
    }
}

function co_hosts(self){
    var main = document.getElementById('main');
    var container = document.getElementById('container');
    var element = document.createElement('div');
    var controls = document.getElementById('controls');
    main.style.gridTemplateRows = "auto 200px 110px";
    controls.style.gridRow = "3 / 4";
    element.setAttribute('id','co_hosts');
    container.insertAdjacentElement('beforebegin',element);
}

function form_handler(ev){
    ev.preventDefault();
    var chats;
    var stream_title = ev.target.firstElementChild.value;
    var description = ev.target.children[2].value;
    var radio_button1 = document.getElementById('enable_chats');
    var submit_button = ev.target.lastElementChild;
    submit_button.innerHTML = "Starting session...";
    if (radio_button1.checked){
        chats = false;
        var parent = document.getElementById('main');
        var child = document.getElementById('comments').parentElement;
        parent.removeChild(child);
        var parent = document.getElementById('container').firstElementChild;
        var child = parent.children[2];
        parent.removeChild(child);
    }else {
        chats = true;
    }
    fetch(window.location,{
        method: 'POST',
        body: JSON.stringify({'stream_title':stream_title,'description':description,'chats':chats}),
        headers: {
            'Content-type':'application/json',
            'X-Requested-With':'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    session_title = stream_title;
    session_description = description;
    var info = `<h3>${session_title}</h3>
    <p>${session_description}</p>
    `
    document.getElementById('session_info').innerHTML = info + document.getElementById('session_info').innerHTML;
    document.getElementById('stream_description').style.display = 'none';
    let websocket_url = `${connection_protocol}://${window.location.host}/meet/${CHANNEL}/${UID}/${role}/`;
    socket = new WebSocket(websocket_url);
    socket.addEventListener('message',getSocketMessages);
    joinAndDisplayLocalStream();
    recognition.start();
}

function session_info(){
    document.getElementById('session_info').style.display = "flex";
}

function getCookie(name){
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

function add_comment_by_enter (event) {
    if (event.keyCode == 13){
        var self = document.getElementById('comments').lastElementChild.lastElementChild;
        add_comment(self);
    }
}

function close_comments(self){
    self.parentElement.parentElement.style.display = 'none';
    var main = document.getElementById('main');
    main.style.gridTemplateColumns = "auto";
    var button = document.getElementById('container').firstElementChild.children[2];
    button.innerHTML = '<i class = "far fa-comments"></i>';
}

function close_items(self){
    self.parentElement.parentElement.style.display = "none";
}

function view_description(self){
    var description = document.getElementById('stream_description');
    description.style.display = "flex";
}

function stop_live_stream(self){
    localTracks.forEach(item => {
        item.stop();
        item.close();
    }) 
    client.leave();
    window.location = "/live_ended";
}

window.addEventListener('beforeunload',() => {
    localTracks.forEach(item => {
        item.stop();
        item.close();
    }) 
    client.leave();
});



