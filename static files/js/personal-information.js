document.getElementById('select-image').addEventListener('click', () => {
	document.getElementById('profile_picture').click();
})

document.getElementById('profile_picture').addEventListener('change', (event) => {
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

			document.getElementById('crop').addEventListener('click', function () {
			    var croppedCanvas = cropper.getCroppedCanvas();
			    if (croppedCanvas) {
			        var croppedImageDataUrl = croppedCanvas.toDataURL('image/png');
			        var image = document.createElement('img');
			        image.setAttribute('src', croppedImageDataUrl);
			        image.setAttribute('class','mr-3 border border-gray-300 rounded-full h-14 sm:h-9');
			        image.setAttribute('alt', 'Profile Picture');
			        image.setAttribute('name', 'personal_information-profile_picture');
			        image.setAttribute('id', 'id_personal_information-profile_picture');
			        image.setAttribute('value', croppedImageDataUrl);

			        var oldChild = document.getElementById('avatar-image');

			        oldChild.parentNode.replaceChild(image, oldChild);

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
	document.getElementById('id_personal_information-profile_picture').value = '';
})

var tagify = new Tagify(document.getElementById('skills'));

document.getElementById('form').addEventListener('submit', () => {
	var tags = tagify.getCleanValue().map(tag => tag.value);
	document.getElementById('id_personal_information-skills').value = JSON.stringify(tags.join(','));
})