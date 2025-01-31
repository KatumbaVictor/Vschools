document.getElementById('add-requirement-field').addEventListener('click', () => {
	let container;
	var div = document.createElement('div');
	div.setAttribute('class', 'flex items-center gap-2 mt-4 mb-2');

	var input_field = document.createElement('input');
	input_field.setAttribute('type', 'text');
	input_field.setAttribute('name', 'responsibilities')
	input_field.setAttribute('placeholder', 'Add a responsibility, e.g., Manage project timelines and deliverables.')
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
    	document.getElementById('responsibilitiesContainer').removeChild(div);
    })

    document.getElementById('responsibilitiesContainer').appendChild(div);
})

let first_input = document.getElementById('responsibilitiesContainer').firstElementChild.firstElementChild;

first_input.addEventListener('input', () => {
	if (first_input.value.length != 0) {
		document.getElementById('add-requirement-field').removeAttribute('disabled');
		document.getElementById('add-requirement-field').classList.remove('bg-blue-400');
		document.getElementById('add-requirement-field').classList.add('bg-blue-700');
		document.getElementById('add-requirement-field').classList.add('focus:ring-4');
		document.getElementById('add-requirement-field').classList.remove('cursor-not-allowed');
	} else {
		document.getElementById('add-requirement-field').setAttribute('disabled', '');
		document.getElementById('add-requirement-field').classList.remove('bg-blue-700');
		document.getElementById('add-requirement-field').classList.remove('focus:ring-4');
		document.getElementById('add-requirement-field').classList.add('cursor-not-allowed');
		document.getElementById('add-requirement-field').classList.add('bg-blue-400');
	}
})


document.getElementById('form').addEventListener('submit', (event) => {
	let inputs = document.querySelectorAll("input[name='responsibilities']");

	let responsibilities_list = [];
	inputs.forEach((input) => {
		if (input.value.trim() !== "") {
			responsibilities_list.push(input.value.trim());
		}
	})

	document.getElementById('id_job-details-key_responsibilities').value = JSON.stringify(responsibilities_list);

})