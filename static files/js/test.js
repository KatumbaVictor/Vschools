var image = document.getElementById('image');
//var croppedImageElement = document.getElementById('croppedImage');


var cropper = new Cropper(image, {
    aspectRatio: 1,
    viewMode: 1
})


document.getElementById('crop').addEventListener('click', function () {
    var croppedCanvas = cropper.getCroppedCanvas();
    if (croppedCanvas) {
        var croppedImageDataUrl = croppedCanvas.toDataURL('image/png');
        console.log(croppedImageDataUrl)
    }
})

document.getElementById('modal-button').addEventListener('click', function() {
    document.getElementById('logout-modal').style.visibility = "visible"
})