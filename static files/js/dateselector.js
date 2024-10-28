Array.from(document.getElementsByClassName('dateselector')).forEach((datepickerElement) => {
	const datepickerOptions = {
		autohide: true,
		buttons: true,
		format: 'dd/mm/yyyy',
		title: 'Date of birth'
	}

	const datePicker = new Datepicker(datepickerElement, datepickerOptions);
})