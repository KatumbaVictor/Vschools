const endorsement_form = document.getElementById('endorsement-form');


endorsement_form.addEventListener('submit', (e) => {
	e.preventDefault();
	const formData = new FormData(endorsement_form);
	const url = endorsement_form.action;

	fetch(url, {
		method: 'POST',
		body: formData,
		headers: {
			'X-CSRFToken': getCookie('csrftoken'),
			'X-Requested-With': 'XMLHttpRequest',
			'Accept': 'application/json',
		},
		body: formData,
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