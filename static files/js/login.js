const form = document.getElementById('login-form');

form.addEventListener('submit', () => {
	const submit_button = document.getElementById('submit-button');
	submit_button.innerHTML = "Logging into account...."
	submit_button.classList.remove('bg-blue-700');
	submit_button.classList.remove('focus:ring-blue-300');
	submit_button.classList.remove('hover:bg-blue-800');
	submit_button.classList.add('bg-blue-400')
	submit_button.classList.add('cursor-not-allowed');
	submit_button.setAttribute('disabled', '');
})