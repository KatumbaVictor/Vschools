var meetingTitle = '';
var meetingDescription = '';
var frequency = document.getElementById('frequency').value;
var startDate = '';
var startTime = '';
var meetingEndTime = '';

var daysOfWeek = [];
var weeksOfMonth = [];

const form = new FormData();

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


const today = new Date().toISOString().split('T')[0];
document.getElementById('date_input').setAttribute('min',today);

var getSelectedDate = (self) => {
    let date = new Date(self.value);
    document.getElementById(`day_${date.getDay().toString()}`).click();
    startDate = self.value;
}

let getFrequency = (self) => {
    var element_one = document.getElementById('daysOfWeek');
    var element_two = document.getElementById('weeksOfMonth');
    var items = [element_one, element_two, element_one.previousElementSibling, element_two.previousElementSibling];

    if (self.value === 'Repeat every week') {
        element_one.style.display = "flex";
        element_one.previousElementSibling.style.display = "block";
    }else if (self.value === 'Repeat every month') {
        items.forEach((item) => {
            item.style.display = "flex";
        })
    }else {
        items.forEach((item) => {
            item.style.display = "none";
        })
    }
    frequency = self.value;
}

let setTitle = (self) => {
    meetingTitle = self.value;
}

let setDescription = (self) => {
    meetingDescription = self.value;
}

let getStartTime = (self) => {
    startTime = self.value;
}

let getMeetingEndTime = (self) => {
    meetingEndTime = self.value;
}

let handleDay = (self) => {
    if (self.checked) {
        daysOfWeek.push(self.dataset.name);
    }else {
        daysOfWeek = daysOfWeek.filter(item => item !== self.dataset.name);
    }
}

let handleWeek = (self) => {
    if (self.checked) {
        weeksOfMonth.push(self.dataset.name);
    }else {
        weeksOfMonth = weeksOfMonth.filter(item => item !== self.dataset.name);
    }
}

let submitSchedule = (ev) => {
    ev.preventDefault();
    var submit_button = document.getElementById('submit_button');
    submit_button.innerHTML = '<i class = "far fa-calendar"></i> Scheduling...';
    submit_button.style.color = 'rgba(255, 255, 255, 0.889)'

    form.append('meetingTitle', meetingTitle);
    form.append('meetingDescription', meetingDescription);
    form.append('frequency', frequency);
    form.append('startDate', startDate);
    form.append('startTime', startTime);
    form.append('meetingEndTime', meetingEndTime);

    if (daysOfWeek.length > 0) {
        form.append('daysOfWeek', JSON.stringify(daysOfWeek));
    }

    if (weeksOfMonth.length > 0) {
        form.append('weeksOfMonth', JSON.stringify(weeksOfMonth));
    }

    fetch(window.location,{
        method: 'POST',
        headers:{
            "X-CSRFToken": csrftoken,
            'X-Requested-With':'XMLHttpRequest'
        },
        body: form
    }).then((response) => {
        return response.json().then((data) => {
            var token = data.tokenValue;
            window.open(`/scheduled-meeting/${token}`,'_self');
        })
    })

}