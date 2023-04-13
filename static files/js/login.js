const form = document.getElementById('form');
form.addEventListener('submit',() => {
    var button = form.lastElementChild;
    button.innerHTML = "LOGGING IN....";
    button.setAttribute('disabled','');
    button.style.color = 'rgba(255, 255, 255, 0.889)';
})

let close_item = () => {
    document.getElementById('forgot_password').style.display = "none";
}

setTimeout(() => {
    var element = Array.from(document.getElementsByClassName('wrong_details'))[0];
    element.style.opacity = "0";
},5000)