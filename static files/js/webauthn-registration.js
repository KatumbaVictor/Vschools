const username = document.getElementById('navbar').dataset.username;
const email = document.getElementById('navbar').dataset.email;
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const form = new FormData();

var address;

/*$(document).ready(function() {
    $('.tooltipped').tooltip()
    $('.model').model()
})*/

if (window.location.protocol != 'https:') {
    address = 'localhost:8000'
}else {
    address = window.location.hostname;
}

const create_credential = () => {
    var url = new URL(`${window.location.protocol}//${address}/webauthn-registration-options`);

    const request = new Request(url, {
        method: 'GET',
    })

    fetch(request).then((response) => {
        return response.json().then((data) => {
            data.publicKey.challenge = base64url.decode(data.publicKey.challenge);
            data.publicKey.user.id = base64url.decode(data.publicKey.user.id);
            data.publicKey.authenticatorSelection = {"authenticatorAttachment": "platform", "residentKey": "preferred", "requireResidentKey": false}

            complete_registration(data);
        })
    })
}

const complete_registration = (data) => {
    if (typeof navigator.credentials !== 'undefined') {
          navigator.credentials.create(data)
            .then(credentialInfo => {
                var item = publicKeyCredentialToJSON(credentialInfo);

                form.append('credential', JSON.stringify(item))

                fetch('/webauthn-verify-registration/',{
                    method: 'POST',
                    headers: {'X-Requested-With':'XMLHttpRequest',
                            'X-CSRFToken': csrftoken},
                    body: form
                }).then((response) => {
                    if (response.ok) {
                        var element = document.getElementById('modelWrapper');
                        element.style.display = "block";
                        
                        setTimeout(() => {
                            window.open('/webauthn-registration-complete/','_self');
                        }, 6000)
                    }
                })
            })
    }
}

let check_passkeys = () => {

}

/*
function check_passkey(platform_authenticator = true,success_func, fail_func) { 
    if (platform_authenticator) { 
        PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable()
        .then((available) => { 
            if (available) {
                success_func(); } 
            else{ fail_func(); } }) } success_func(); } 
            function check_passkeys(success_func, fail_func) {
             PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable() 
             .then((available) => {
              if (available) { success_func(); } 
             else { fail_func() } }).catch((err) => 
             { // Something went wrong console.error(err); }); }
*/