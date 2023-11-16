const username = document.getElementById('navbar').dataset.username;

var string = `${window.location.protocol}//${window.location.host}`;
var url = new URL(string);
var host = url.host.replace('dialogue.','');

//const profile_picture = `${window.location.protocol}//${host}${document.getElementById('navbar').getAttribute('data-profilePic')}`;
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
var userLocation;

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
            getMessage(response);
        }else if (response.file_info) {
            var item = response.file_info;
            file_details.push(response)
        }else if (response.joined) {
            if (response.id != userID) {
                showNotification(`${response.username} has joined`);
                var container = document.createElement('div');
                container.setAttribute('class','user');
                container.setAttribute('id',`user_${response.id}`)
                container.innerHTML = `
                    <img src = '${response.profile_picture}'/>
                    <p>${response.username}</p>
                `
                var parent = document.getElementsByClassName('chats')[0];
                parent.append(container);

                var heading = document.getElementById('header').firstElementChild;
                heading.innerHTML = `${parent.children.length - 1} Participants`

                var button = document.getElementsByClassName('people')[0];
                button.innerHTML = `${parent.children.length - 1} participants`;
                
            }
        }else if (response.recording_audio) {
            if (response.id != userID) {
                showNotification(`${response.username} is recording audio...`);
            }
        }else if (response.typing) {
            if (response.id != userID) {
                showNotification(`${response.username} is typing...`);
            }
        }else if (response.user_left) {
            showAlert(`${response.username} has left`);
            document.getElementById(`user_${response.id}`).remove();

            var parent = document.getElementsByClassName('chats')[0];

            if (parent.children.length === 1) {
                var heading = document.getElementById('header').firstElementChild;
                heading.innerHTML = '1 Participant'

                var button = document.getElementsByClassName('people')[0];
                button.innerHTML = '1 participant';
            }
        }else if (response.users) {
            var parent = document.getElementsByClassName('chats')[0];

            response.users.forEach((item) => {
                var container = document.createElement('div');
                container.setAttribute('class','user');
                container.setAttribute('id',`user_${item.id}`)
                container.innerHTML = `
                    <img src = '${item.profile_picture}'/>
                    <p>${item.username}</p>
                `
                parent.append(container);

                var heading = document.getElementById('header').firstElementChild;
                heading.innerHTML = `${parent.children.length - 1} Participants`

                var button = document.getElementsByClassName('people')[0];
                button.innerHTML = `${parent.children.length - 1} participants`;
            })
        }else if (response.delete) {
            var element = document.getElementById(`${response.messageID}`);
            element.remove();
        }else if (response.update) {
            var element = document.getElementById(`${response.messageID}`).children[2];
            element.innerHTML = response.message;
        }
    }
}

socket.onopen = () => {
    var item = {'username':username,'joined':true, 'id':userID,'profile_picture':profile_picture};
    socket.send(JSON.stringify(item));
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
    container.setAttribute('id',data.messageID);

    var message_time = getTime();

    if (data.location) {
        message_time += ` | ${data.location}`;
    }


    if (expression.test(data.text_value) == true) {
        data.text_value = data.text_value.replace(expression, (url) => {
            return `<a href = '${url}' target="_blank">${url}</a>`;
        })
    }

    container.innerHTML = `
        <img src = "${data.profile_picture}" class = "profile_picture" alt = "profile photo"/>
        <p style = "margin-bottom: 0;" class = "username">${data.username} <span>${message_time}</span></p>
        <p class = "right">${data.text_value}</p>
    `

    if (data.id === userID) {
        container.innerHTML += `
            <div>
                <button title = "Delete message" onclick = "deleteMessage('${data.messageID}')">
                    <i class = "fas fa-trash"></i>
                </button>
                <button title = "Edit message" onclick = "editMessage(this, '${data.messageID}')">
                    <i class = "fas fa-pen"></i>
                </button>
            </div>
        `
    }

    var body = document.body;
    body.appendChild(container)
    window.scrollTo(0, document.body.scrollHeight);

    if (data.id != userID) {
        if ('vibrate' in navigator) {
            navigator.vibrate(100);
        }
    }
}

let deleteMessage = (messageID) => {
    var item = {'delete':true, 'messageID':messageID, 'userID':userID};
    socket.send(JSON.stringify(item));
    showAlert('<i class = "fas fa-trash"></i> Your message has been successfully deleted');
}

let editMessage = (self, messageID) => {
    var element = document.getElementById(messageID).children[2];
    element.setAttribute('contenteditable','');
    showNotification('<i class = "fas fa-pen"></i> Click and edit your message.');

    self.innerHTML = '<i class = "fas fa-paper-plane"></i>';
    self.setAttribute('onclick',`updateMessage(this, '${messageID}')`);
    self.setAttribute('title','Update message');
}

let updateMessage = (self, messageID) => {
    var element = document.getElementById(messageID).children[2];
    element.removeAttribute('contenteditable');
    showNotification('Your message has been successfully updated.');
    self.innerHTML = '<i class = "fas fa-pen"></i>';
    self.setAttribute('onclick',`editMessage(this, '${messageID}')`);
    self.setAttribute('title','Edit message');

    var item = {'update':true, 'messageID':messageID, 'message': element.innerHTML};
    socket.send(JSON.stringify(item));
}

let postMessage = (self) => {
    var text_value = self.parentElement.children[3].value;
    var parent = document.getElementsByTagName('main')[0];
    var messageID = (Math.random() * 10).toString(36).replace('.','');
    
    if (text_value.length > 0) {
        self.parentElement.children[3].value = "";

        var item = {'profile_picture':profile_picture, 'username': username, 'text_value':text_value,
                    'id': userID, 'messageID':messageID};

        if (userLocation != undefined) {
            item.location = userLocation;
        }

        socket.send(JSON.stringify(item));
    }else {
        showAlert('<i class = "fas fa-exclamation-triangle"></i> You cannot send an empty message');
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
    item.style.backgroundColor = 'rgb(255, 220, 220)';
    item.innerHTML = data;
    item.style.opacity = "1";
    setTimeout(() => {
        item.style.opacity = "0";
    },4000)
}

let showNotification = (data) => {
    var item = document.getElementById('alert');
    item.style.backgroundColor = 'rgb(173,216,230)'
    item.innerHTML = data;
    item.style.opacity = "1";
    setTimeout(() => {
        item.style.opacity = "0";
    },5000)

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

let typeNotifier = (self) => {
    if (self.value.length === 3) {
        var indicator = {'username':username,'typing':true,'id':userID};
        socket.send(JSON.stringify(indicator));
    }
}

let listenAudio = () => {
    recordedChunks = [];
    
    if (audioInputDevices.length > 0) {
        navigator.mediaDevices.getUserMedia({ audio: true })
        .then((stream) => {
            mediaStream = stream;
            mediaRecorder = new MediaRecorder(stream);

            document.getElementById('audio_panel').style.display = "block";

            var indicator = {'username':username,'recording_audio':true,'id':userID}
            socket.send(JSON.stringify(indicator));

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

    showNotification('<i class = "fas fa-copy"></i> Link copied to clipboard');

    setTimeout(() => {
        self.innerHTML = 'Copy link <i class = "far fa-copy"></i>'
    }, 3000)
}

let view_users = () => {
    document.getElementById('participants').style.display = "flex";
}

let close = () => {
    alert('hello')
    document.getElementById('participants').style.display = "none";
}

let detachLocation = (self) => {
    self.setAttribute('onclick','getLocation(this)');
    showNotification('Location detached');
}

let getLocation = (self) => {
    if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition((position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            
            const url = new URL(`${window.location.protocol}//${window.location.host}/chat/reverse-geocode/`);

            url.searchParams.append('latitude', latitude);
            url.searchParams.append('longitude', longitude);

            const request = new Request(url, {
                method: 'GET'
            })

            fetch(request)
                .then((response) => {
                    return response.json().then((data) => {
                        var address = data.address;
                        showNotification('Your location will be attached to your messages');
                        self.style.color = "blue";
                        userLocation = address;
                        self.setAttribute('onclick','detachLocation(this)');
                    })
                })
        })
    }
}

window.addEventListener('offline', () => {
    showAlert('<i class = "fas fa-exclamation-triangle"></i> You are currently offline, Please check your internet connection');
})

window.addEventListener('online', () => {
    showNotification('You are now back online, your internet connection has been restored.');
})

let notifications = (self) => {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/js/worker.js')
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
    }
}
