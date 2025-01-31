const form = document.getElementById('form');

form.addEventListener('submit', (e) => {
	e.preventDefault();

	var formData = new FormData(form);

	fetch(form.dataset.update_url, {
		method: "POST",
		headers: {
			"X-Requested-With": "XMLHttpRequest",
			"X-CSRFToken": formData.get("csrfmiddelwaretoken"),
		},
		body: formData
	}).then((response) => {
		if (!response.ok) {
			return response.json().then((data) => {
				throw data;
			});
		}

		return response.json();
	})
	.then((data) => {
		const successButton = document.getElementById('successButton');
		successButton.click();
	})
})