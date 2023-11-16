const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
var image_cropper;

const original_name = document.getElementById('username').value;

 
function get_photo(){
    var file_button = document.getElementById('photo');
    file_button.click();
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

function cancel() {
    document.getElementById('cropper_holder').style.display = "none";
}

function crop(){
    image_cropper.getCroppedCanvas().toBlob((blob) => {
        var form = new FormData();
        form.append("image",blob);
        fetch(window.location,{
            method: "POST",
            headers: { 
                    "X-CSRFToken": csrftoken,
                    'X-Requested-With':'XMLHttpRequest'},
            body: form
        })
        var image = document.getElementById('divtwo').firstElementChild;
        image.setAttribute('src',URL.createObjectURL(blob));
    })
    document.getElementById('cropper_holder').style.display = "none";
}

let change_password = () => {
    var password_one = document.getElementById('password_one').value;
    var password_two = document.getElementById('password_two').value;

    if (password_one === password_two) {
        fetch('/update_password/',{
            method: 'POST',
            headers: { 'Accept': 'application/json',
                    'X-Requested-With':'XMLHttpRequest',
                    'X-CSRFToken': csrftoken},
            body: JSON.stringify({'password_one':password_one,'password_two':password_two})
        })
    }
}

let update_info = (ev) => {
    ev.preventDefault();
    var username = document.getElementById('username').value;
    var button = document.getElementById('form').lastElementChild;

    fetch('/update_username/',{
        method: 'POST',
        headers: { 'Accept': 'application/json',
                'X-Requested-With':'XMLHttpRequest',
                'X-CSRFToken': csrftoken},
        body: JSON.stringify({'username':username})
    }).then(() => {
        button.innerHTML = "Updating...";
        setTimeout(() => {
            button.innerHTML = "Update info";
            var notification_panel = document.getElementById('notification');
            notification_panel.innerHTML = 'Account info updated...'
            notification_panel.style.opacity = '1';

            setTimeout(() => {
                notification_panel.style.opacity = '0';
            }, 4000)

        }, 3000)
    })

    var password_one = document.getElementById('password_one').value;
    var password_two = document.getElementById('password_two').value;

    if (password_one.length != 0 && password_two.length != 0) {
        change_password();
    }

}

function back() {
    window.open('/login/','_self');
}