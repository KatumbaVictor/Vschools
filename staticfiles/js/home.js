var passcode_field = document.getElementById('passcode_field');
const page_options = document.getElementById('options');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

//page_options.style.display = "none";

function start_meeting(self){
    self.innerHTML = '<i class = "fas fa-plus"></i> Starting meeting...';
    self.style.color = 'rgba(255, 255, 255, 0.889)';

    fetch('/start_meeting/',{
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            "X-CSRFToken": csrftoken,
            'X-Requested-With':'XMLHttpRequest'
        },
        body: JSON.stringify({'start_meeting':'True'})
    }).then((response) => {
        return response.json().then((data) => {
            window.open(`/meet/${data.meeting_id}`,'_self');
        })
    })
}

let join_meeting = (self) => {
    self.preventDefault();
    self.innerHTML = "Checking meeting..."
    var passcode = self.target.firstElementChild.value;
    var button = self.target.lastElementChild;

    fetch(`/join_session/?passcode=${passcode}`,{
        method: 'GET'
    }).then(response => {
        return response.json().then(data => {
            if (data.meeting_id){
                button.innerHTML = "joining";
                button.setAttribute('disabled','');
                button.style.color = 'rgba(0, 0, 200, 0.44)';
                window.open(`/meet/${data.meeting_id}`,'_self');
            }else {
                document.getElementById('notification').style.opacity = "1";
                setTimeout(() => {
                    document.getElementById('notification').style.opacity = "0";
                },4000)
            }
        })
    })
}

let input_focus = (self) => {
    var button = self.parentElement.lastElementChild;

    if (self.value.length == 0) {
        button.style.color = 'rgba(128, 128, 128, 0.50)';
        button.setAttribute('disabled','');
    }
}

let input_blur = (self) => {
    var button = self.parentElement.lastElementChild;

    if (self.value.length == 0) {
        button.style.color = 'white';
        button.setAttribute('disabled','');
    }
}

let check_passcode = (self) => {
    var button = self.parentElement.lastElementChild;

    if (self.value.length > 0) {
        button.style.color = 'blue';
        button.removeAttribute('disabled');
    }else {
        button.style.color = 'rgba(128, 128, 128, 0.45)';
        button.setAttribute('disabled','');
    }
}

let options = () => {
    if (page_options.style.display == "none"){
        page_options.style.display = "flex";
    }else {
        page_options.style.display = "none";
    }
}

let logout = () => {
    page_options.style.display = "none";
    window.open('/logout/','_self');
}

let scheduled_meetings = () => {
    var user_token = document.getElementById('navbar').dataset.user_token;
    page_options.style.display = "none";
    window.open(`/scheduled-meetings/`,'_self');
}

let settings = () => {
    page_options.style.display = "none";
    window.open('/settings/','_self');
}

passcode_field.onpaste = (e) => {
    var button = passcode_field.parentElement.lastElementChild;
    button.removeAttribute('disabled');
    setTimeout(() => {
        button.click();
    }, 300)
}