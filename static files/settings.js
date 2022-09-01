var image_cropper;

function get_photo(){
    var file_button = document.getElementById('photo');
    file_button.click();
}

function change_password(){
    var current_password = document.getElementById('current_password');
    var new_password1 = document.getElementById('new_password1');
    var new_password2 = docucment.getElementById('new_password2');
}

function crop_photo(self){
    if (self.files){
        var file_reader = new FileReader();
        file_reader.onloadend = function(response){
            const image = document.getElementById('picture');
            image.setAttribute('src',response.currentTarget.result);
            const cropper = new Cropper(image, {
                aspectRatio: 9 / 9,
                crop(event) {},
                })
                image_cropper = cropper;
                document.getElementById('cropper_holder').style.display = "flex";
        }
        file_reader.readAsDataURL(self.files[0]);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function crop(){
    image_cropper.getCroppedCanvas().toBlob((blob) => {
        var form = new FormData();
        form.append("image",blob);
        console.log(URL.createObjectURL(blob));
        fetch(window.location,{
            method: "POST",
            headers: { 'Accept': 'application/json',
                    "X-CSRFToken": getCookie('csrftoken'),
                    'X-Requested-With':'XMLHttpRequest'},
            body: form
        })
        var image = document.createElement('img');
        image.setAttribute('src',URL.createObjectURL(blob));
        var parent = Array.from(document.getElementsByClassName('info_holder'))[0].firstElementChild;
        var child = Array.from(document.getElementsByClassName('info_holder'))[0].firstElementChild.firstElementChild;
        parent.replaceChild(image,child);
    })
    document.getElementById('cropper_holder').style.display = "none";
}

document.getElementById('cancel').addEventListener('click',() => {
    document.getElementById('cropper_holder').style.display = "none";
})