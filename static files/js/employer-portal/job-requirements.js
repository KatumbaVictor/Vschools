var language_tags = new Tagify(document.getElementById('languages_required'));
var skills_tags = new Tagify(document.getElementById('skills'));


var certifications_and_licenses = document.getElementById('certifications_and_licenses');
 

var add_certifications_button = document.getElementById('add-certifications-field');

add_certifications_button.addEventListener('click', () => {
	let container;
	var div = document.createElement('div');
	div.setAttribute('class', 'flex items-center gap-2 mt-4 mb-2');

	var input_field = document.createElement('input');
	input_field.setAttribute('type', 'text');
	input_field.setAttribute('name', 'certifications_and_licenses');
	input_field.setAttribute('placeholder', 'Add a required certification or license');
	input_field.setAttribute('class','flex-1 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500');
	input_field.setAttribute('required', '');

	var button = document.createElement('button');
	button.setAttribute('type', 'button');
	button.setAttribute('class', 'removeReq text-red-500 hover:text-red-700');
	button.innerHTML = `<svg class="w-6 h-6 text-red-500 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14"/>
                        </svg>`;

    div.appendChild(input_field);
    div.appendChild(button);

    button.addEventListener('click', () => {
    	document.getElementById('certificationsContainer').removeChild(div);
    })

    document.getElementById('certificationsContainer').appendChild(div);
})

certifications_and_licenses.addEventListener('input', () => {

	if (certifications_and_licenses.value.length != 0) {
		add_certifications_button.removeAttribute('disabled');
		add_certifications_button.classList.remove('bg-blue-400');
		add_certifications_button.classList.add('bg-blue-700');
		add_certifications_button.classList.add('focus:ring-4');
		add_certifications_button.classList.remove('cursor-not-allowed');
	}else {
		add_certifications_button.setAttribute('disabled', '');
		add_certifications_button.classList.remove('bg-blue-700');
		add_certifications_button.classList.remove('focus:ring-4');
		add_certifications_button.classList.add('cursor-not-allowed');
		add_certifications_button.classList.add('bg-blue-400');
	}
})





var add_requirements_button = document.getElementById('add-requirement-field');
var requirements = document.getElementById('requirements-field');


add_requirements_button.addEventListener('click', () => {
	let container;
	var div = document.createElement('div');
	div.setAttribute('class', 'flex items-center gap-2 mt-4 mb-2');

	var input_field = document.createElement('input');
	input_field.setAttribute('type', 'text');
	input_field.setAttribute('name', 'requirements');
	input_field.setAttribute('placeholder', 'Add an essential requirement');
	input_field.setAttribute('class','flex-1 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500');
	input_field.setAttribute('required', '');

	var button = document.createElement('button');
	button.setAttribute('type', 'button');
	button.setAttribute('class', 'removeReq text-red-500 hover:text-red-700');
	button.innerHTML = `<svg class="w-6 h-6 text-red-500 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14"/>
                        </svg>`;

    div.appendChild(input_field);
    div.appendChild(button);

    button.addEventListener('click', () => {
    	document.getElementById('requirementsContainer').removeChild(div);
    })

    document.getElementById('requirementsContainer').appendChild(div);
})



requirements.addEventListener('input', () => {

	if (requirements.value.length != 0) {
		add_requirements_button.removeAttribute('disabled');
		add_requirements_button.classList.remove('bg-blue-400');
		add_requirements_button.classList.add('bg-blue-700');
		add_requirements_button.classList.add('focus:ring-4');
		add_requirements_button.classList.remove('cursor-not-allowed');
	}else {
		add_requirements_button.setAttribute('disabled', '');
		add_requirements_button.classList.remove('bg-blue-700');
		add_requirements_button.classList.remove('focus:ring-4');
		add_requirements_button.classList.add('cursor-not-allowed');
		add_requirements_button.classList.add('bg-blue-400');
	}
})


document.getElementById('form').addEventListener('submit', () => {
	var tags_one = language_tags.getCleanValue().map(tag => tag.value);
	document.getElementById('id_job-requirements-languages_required').value = JSON.stringify(tags_one.join(','));

	var tags_two = skills_tags.getCleanValue().map(tag => tag.value);
	document.getElementById('id_job-requirements-required_skills').value = JSON.stringify(tags_two.join(','));

	let certifications_inputs = document.querySelectorAll("input[name='certifications_and_licenses']");

	let certifications_list = [];
	certifications_inputs.forEach((input) => {
		if (input.value.trim() !== "") {
			certifications_list.push(input.value.trim());
		}
	})

	document.getElementById('id_job-requirements-certifications_and_licenses').value = JSON.stringify(certifications_list);


	let requirements_inputs = document.querySelectorAll("input[name='requirements']");

	let requirements_list = [];
	requirements_inputs.forEach((input) => {
		if (input.value.trim() !== "") {
			requirements_list.push(input.value.trim());
		}
	})

	document.getElementById('id_job-requirements-additional_requirements').value = JSON.stringify(requirements_list);
})