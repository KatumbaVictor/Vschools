function create_meeting(self){
    window.open(`/meet/${self.dataset.user_token}`,'_self');

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
                button.style.color = 'rgba(0, 0, 200, 0.44)';
                window.open(`/meet/${data.meeting_id}`,'_self');
            }else {
                document.getElementById('notification').style.opacity = "1";
                setTimeout(() => {
                    document.getElementById('notification').style.opacity = "0";
                }, 2000)
            }
        })
    })
}