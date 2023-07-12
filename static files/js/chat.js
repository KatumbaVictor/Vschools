const username = document.getElementById('navbar').dataset.username;
const profile_picture = document.getElementById('navbar').getAttribute('data-profilePic');
const room_name = document.getElementById('navbar').dataset.usertoken;
var connection_protocol;
var socketUrl;

if (window.location.protocol == 'https:'){
    connection_protocol = 'wss';
    socketUrl = `${connection_protocol}://${window.location.host}:8001/ChatSocket/${room_name}/`;
}else {
    connection_protocol = 'ws';
    socketUrl = `${connection_protocol}://${window.location.host}/ChatSocket/${room_name}/`;
}

const socket = new WebSocket(socketUrl);

socket.onmessage = (e) => {
    var response = JSON.parse(e.data);

    if (response.text_value) {
        getMessage(response)
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

let getMessage = (data) => {
    var container = document.createElement('div');
    var parent = document.getElementsByTagName('main')[0];
    container.setAttribute('class','message');
    container.innerHTML = `
        <img src = "${data.profile_picture}" alt = "profile photo"/>
        <p style = "margin-bottom: 0;"><span>${data.username}</span></p>
        <p class = "right">${data.text_value}</p>
    `

    parent.appendChild(container)
}

let postMessage = (self) => {
    var text_value = self.parentElement.firstElementChild.value;
    var parent = document.getElementsByTagName('main')[0];
    
    if (text_value.length > 0) {
        self.parentElement.firstElementChild.value = "";
        parent.scrollTop = parent.scrollHeight;

        var item = {'profile_picture':profile_picture, 'username': username, 'text_value':text_value};
        socket.send(JSON.stringify(item));
    }
}

let SendWithEnter = (keyboard_event) => {
    if (keyboard_event.keyCode == 13){
        var self = document.getElementById('sendButton');
        postMessage(self);
    }
}

let likeButton = (self) => {
    self.firstElementChild.setAttribute('class','fas fa-thumbs-up')
    self.setAttribute('onclick','unlikeButton(this)');
}

let unlikeButton = (self) => {
    self.firstElementChild.setAttribute('class','far fa-thumbs-up');
    self.setAttribute('onclick','likeButton(this)');
}