let agree = () => {
	window.open('/','_self');
}

let handleCheckbox = (self) => {
	var button = document.getElementById('agreeButton');

	if (self.checked) {
		button.removeAttribute('disabled');
	}else {
		button.setAttribute('disabled','');
	}
}