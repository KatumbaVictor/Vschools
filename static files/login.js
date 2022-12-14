const form = document.getElementById('form');
form.addEventListener('submit',() => {
    var button = form.lastElementChild;
    button.innerHTML = "LOGGING IN....";
    button.setAttribute('disabled','');
    button.style.color = 'rgba(245, 245, 245, 0.74)';
})

let close_item = () => {
    document.getElementById('forgot_password').style.display = "none";
}
