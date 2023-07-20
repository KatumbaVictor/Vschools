const username = document.getElementById('navbar').dataset.username;
const profile_picture = document.getElementById('navbar').getAttribute('data-profilePic');
const room_name = window.location.pathname.split('/').pop();
var connection_protocol;
var socketUrl;
var files = [];
var file_details = [];

if (window.location.protocol == 'https:'){
    connection_protocol = 'wss';
    socketUrl = `${connection_protocol}://${window.location.host}:8001/ChatSocket/${room_name}/`;
}else {
    connection_protocol = 'ws';
    socketUrl = `${connection_protocol}://${window.location.host}/ChatSocket/${room_name}/`;
}

const socket = new WebSocket(socketUrl);

socket.onmessage = (e) => {
    if (e.data instanceof Blob) {
        var data = e.data;

        var imageURL = URL.createObjectURL(e.data);
        var image = document.createElement('img');
        image.setAttribute('src', imageURL);
        
        files.push(data);

        var index = files.indexOf(data);
        var item = file_details[index];
        item['fileSource'] = URL.createObjectURL(e.data);

        getImage(item);

    }else {
        var response = JSON.parse(e.data);
        if (response.text_value) {
            getMessage(response)
        }else if (response.file_info) {
            file_details.push(response)
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

var date = new Date();
var options = {hour12: true, hour: 'numeric', minute: 'numeric'};
var formattedTime = date.toLocaleTimeString('en-US', options);

let getImage = (data) => {
    var container = document.createElement('div');
    var parent = document.getElementsByTagName('main')[0];
    container.setAttribute('class','message');
    container.innerHTML = `
        <img src = "${data.profile_picture}" class = "profile_picture" alt = "profile photo"/>
        <p style = "margin-bottom: 0;" class = "username">${data.username} <span>${formattedTime}</span></p>
        <img src = "${data.fileSource}" class = "image_post" ondblclick = "ShowFullImage(this)"/>
    `

    parent.appendChild(container)
}

let ShowFullImage = (self) => {
    self.requestFullscreen()
}

let getMessage = (data) => {
    var container = document.createElement('div');
    var parent = document.getElementsByTagName('main')[0];
    container.setAttribute('class','message');
    container.innerHTML = `
        <img src = "${data.profile_picture}" class = "profile_picture" alt = "profile photo"/>
        <p style = "margin-bottom: 0;" class = "username">${data.username} <span>${formattedTime}</span></p>
        <p class = "right">${data.text_value}</p>
    `

    parent.appendChild(container)
}

let postMessage = (self) => {
    var text_value = self.parentElement.children[3].value;
    var parent = document.getElementsByTagName('main')[0];
    
    if (text_value.length > 0) {
        self.parentElement.children[3].value = "";

        var item = {'profile_picture':profile_picture, 'username': username, 'text_value':text_value};

        socket.send(JSON.stringify(item));
    }
}

let postFile = (self) => {
    if (self.files) {
        const reader = new FileReader();
        reader.onload = (event) => {
            const binaryData = event.target.result;
            console.log(binaryData)

            var file_data = {'username':username,'profile_picture':profile_picture,'file_info':'image'};
            socket.send(JSON.stringify(file_data));

            socket.send(binaryData)

        }

        reader.onprogress = (event) => {
            if (event.lengthComputable) {
                document.getElementById('progress').style.display = "flex";
                const progress = Math.trunc((event.loaded / event.total)) * 100;
                const targetElement = document.getElementById('progress').children[1].firstElementChild;
                console.log(progress)
                targetElement.style.width = `${progress}%`;
                document.getElementById('progress').lastElementChild.innerHTML = `${progress}%`
            }
        }

        reader.onloadend = () => {
            document.getElementById('progress').style.display = "none";
        }

        reader.readAsArrayBuffer(self.files[0])
    }
}

let getFile = () => {
    document.getElementById('file').click();
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

let copyLink = (self) => {
    self.innerHTML = 'Copied link <i class = "fas fa-copy"></i>'
    var link = self.parentElement.children[1].value;
    navigator.clipboard.writeText(link);

    setTimeout(() => {
        self.innerHTML = 'Copy link <i class = "far fa-copy"></i>'
    }, 3000)
}