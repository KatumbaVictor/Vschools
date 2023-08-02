const username = document.getElementById('navbar').dataset.username;
const profile_picture = document.getElementById('navbar').getAttribute('data-profilePic');
const expression = /((ftp|http|https):\/\/)(www\.)?([\w]+)(\.[\w]+)+(\/[\w]+)*/g;
const room_name = window.location.pathname.split('/').pop();
const userID = document.getElementById('divone').dataset.id;
var connection_protocol;
var socketUrl;
var files = [];
var file_details = [];
var mediaRecorder;
var mediaStream;
var audioInputDevices;

if (window.location.protocol == 'https:'){
    connection_protocol = 'wss';
    socketUrl = `${connection_protocol}://${window.location.host}:8001/ChatSocket/${room_name}/`;
}else {
    connection_protocol = 'ws';
    socketUrl = `${connection_protocol}://${window.location.host}/ChatSocket/${room_name}/`;
}

navigator.mediaDevices.enumerateDevices()
.then(devices => {
    audioInputDevices = devices.filter(device => device.kind === 'audioinput');
})

const socket = new WebSocket(socketUrl);

socket.onmessage = (e) => {
    if (e.data instanceof Blob) {
        var data = e.data;
        files.push(data);

        var index = files.indexOf(data);
        var item = file_details[index];
        item['fileSource'] = URL.createObjectURL(e.data);

        if (item.id != userID) {
            if (item.file_info === 'image') {
                getImage(item);
            }else if (item.file_info === 'audio') {
                getAudio(item);
            }
        }

    }else {
        var response = JSON.parse(e.data);
        if (response.text_value) {
            getMessage(response)
        }else if (response.file_info) {
            var item = response.file_info;
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

let getTime = () => {
    var date = new Date();
    var options = {hour12: true, hour: 'numeric', minute: 'numeric'};
    var formattedTime = date.toLocaleTimeString('en-US', options);

    return formattedTime;
}

let getImage = (data) => {
    var container = document.createElement('div');
    var parent = document.getElementById('container')
    container.setAttribute('class','message');
    container.innerHTML = `
        <img src = "${data.profile_picture}" class = "profile_picture" alt = "profile photo"/>
        <p style = "margin-bottom: 0;" class = "username">${data.username} <span>${getTime()}</span></p>
        <img src = "${data.fileSource}" class = "image_post" ondblclick = "ShowFullImage(this)"/>
    `

    var body = document.body;
    body.appendChild(container)
    setTimeout(() => {window.scrollTo(0, document.body.scrollHeight);}, 1000);
}

let getAudio = (data) => {
    var container = document.createElement('div');
    var parent = document.getElementById('container')
    container.setAttribute('class','message');
    container.innerHTML = `
        <img src = "${data.profile_picture}" class = "profile_picture" alt = "profile photo"/>
        <p style = "margin-bottom: 0;" class = "username">${data.username} <span>${getTime()}</span></p>
        
        <audio controls>
            <source src = "${data.fileSource}" type = "audio/wav">
        </audio>
    `

    var body = document.body;
    body.appendChild(container)

    setTimeout(() => {window.scrollTo(0, document.body.scrollHeight);}, 1000);
}

let ShowFullImage = (self) => {
    self.requestFullscreen()
}

let getMessage = (data) => {
    var container = document.createElement('div');
    var parent = document.getElementsByTagName('main')[0];
    container.setAttribute('class','message');

    if (expression.test(data.text_value) == true) {
        data.text_value = data.text_value.replace(expression, (url) => {
            return `<a href = '${url}' target="_blank">${url}</a>`;
        })
    }

    container.innerHTML = `
        <img src = "${data.profile_picture}" class = "profile_picture" alt = "profile photo"/>
        <p style = "margin-bottom: 0;" class = "username">${data.username} <span>${getTime()}</span></p>
        <p class = "right">${data.text_value}</p>
    `

    var body = document.body;
    body.appendChild(container)
    window.scrollTo(0, document.body.scrollHeight);
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

            var file_data = {'username':username,'profile_picture':profile_picture,'file_info':'image',
                            id:userID};
            socket.send(JSON.stringify(file_data));

            var blob = new Blob([binaryData], {type: file.type});
            file_data['fileSource'] = URL.createObjectURL(blob);

            getImage(file_data);

            socket.send(binaryData)

        }

        reader.onprogress = (event) => {
            if (event.lengthComputable) {
                document.getElementById('progress').style.display = "flex";
                const progress = Math.trunc((event.loaded / event.total)) * 100;
                const targetElement = document.getElementById('progress').children[1].firstElementChild;
                
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

let showAlert = (data) => {
    var item = document.getElementById('alert');
    item.innerHTML = data;
    item.style.opacity = "1";
    setTimeout(() => {
        item.style.opacity = "0";
    },4000)
}

let checkPermission = () => {
    console.log('hello')
    navigator.permissions.query({name:'microphone'})
    .then(permissionStatus => {
        if (permissionStatus.state === 'granted') {
            console.log('yes')
            return true
        }else if (permissionStatus.state === 'prompt') {
            var data = 'Allow microphone permission first';
            showAlert(data);
        }else {
            var data = '<i class = "fas fa-microphone-slash"></i> Microphone permission is denied';
            showAlert(data);
        }
    })
}

let listenAudio = () => {
    recordedChunks = [];
    
    if (audioInputDevices.length > 0) {
        navigator.mediaDevices.getUserMedia({ audio: true })
        .then((stream) => {
            mediaStream = stream;
            mediaRecorder = new MediaRecorder(stream);

            document.getElementById('audio_panel').style.display = "block";

            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            }

            mediaRecorder.onstop = () => {
                var file_data = {'username':username,'profile_picture':profile_picture,'file_info':'audio', id: userID};
                socket.send(JSON.stringify(file_data));

                socket.send(recordedChunks[0]);

                file_data['fileSource'] = URL.createObjectURL(recordedChunks[0]);
                getAudio(file_data);
            }

            mediaRecorder.start();
        })
    }else {
        var data = '<i class = "fas fa-microphone-slash"></i> No microphone is connected to your device';
        showAlert(data);
    }
}

let sendAudio = () => {
    mediaRecorder.stop();
    mediaStream.getTracks().forEach((item) => {item.stop()})
    document.getElementById('audio_panel').style.display = "none"
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

navigator.serviceWorker.register('/static/js/worker.js', { type: 'module' })
.then((registration) => {
    return registration.pushManager.getSubscription();
})
.then(subscription => {
    if (!subscription) {
        return registration.pushManager.subscribe({ userVisibleOnly: true });
    }
})
.then(subscription => {
    console.log(subscription.endpoint)
})
.catch(error => {
    console.error(error);
})