document.getElementById('select-image').addEventListener('click', () => {
	document.getElementById('id_company_information-profile_picture').click();
})

document.getElementById('id_company_information-profile_picture').addEventListener('change', (event) => {
	const file = event.target.files[0];

	if (file && file.type.startsWith('image/')) {
		const reader = new FileReader();

		reader.onload = (e) => {
			document.getElementById('image').src = e.target.result;

			var cropper = new Cropper(document.getElementById('image'), {
			    aspectRatio: 1,
			    viewMode: 1
			})

			document.getElementById('upload-button').click();

			document.getElementById('crop').addEventListener('click', () => {
				var croppedCanvas = cropper.getCroppedCanvas();
				if (croppedCanvas) {
					var croppedImageDataUrl = croppedCanvas.toDataURL('image/png');
			        var image = document.createElement('img');
			        image.setAttribute('src', croppedImageDataUrl);
			        image.setAttribute('class','mr-3 border border-gray-300 rounded-full h-14 sm:h-9');
			        image.setAttribute('alt', 'Profile Picture');

			        var oldChild = document.getElementById('avatar-image');

			        oldChild.parentNode.replaceChild(image, oldChild);

			        const form  = document.getElementById('form');
			        const formData = new FormData(form);
			        formData.append("company_information-profile_picture", croppedImageDataUrl);

			        setTimeout(() => {
			        	document.getElementById('toast-success').classList.remove("hidden");
			        }, 3000)

			        setTimeout(() => {
			        	document.getElementById('toast-success').classList.add("hidden");
			        }, 14000)
				}
			})
		}

		reader.readAsDataURL(file);
	}
})

document.getElementById('upload-button').addEventListener('click', function() {
    document.getElementById('cropper-modal').style.visibility = "visible";
})

document.getElementById('cancel-cropping').addEventListener('click', () => {
	document.getElementById('id_company_information-profile_picture').value = '';
})