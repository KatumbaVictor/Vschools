const application_invite_form = document.getElementById('ApplicationInviteForm');

application_invite_form.addEventListener('submit', (e) => {
	e.preventDefault();
	const inviteFormData = new FormData(application_invite_form);

	fetch(application_invite_form.action, {
		method: 'POST',
		headers: {
			'X-CSRFToken': getCookie('csrftoken'),
			'X-Requested-With': 'XMLHttpRequest',
			'Accept': 'application/json',
		},
		body: inviteFormData,
	})
	.then(response => response.json())
	.then(data => {

	})
})



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}