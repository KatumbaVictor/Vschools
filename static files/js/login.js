const form = document.getElementById('form');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

form.addEventListener('submit',() => {
    var button = form.lastElementChild;
    button.innerHTML = "LOGGING IN....";
    button.setAttribute('disabled','');
})

let close_item = () => {
    document.getElementById('forgot_password').style.display = "none";
}

/*setTimeout(() => {
    var element = Array.from(document.getElementsByClassName('wrong_details'))[0];
    element.style.opacity = "0";
},5000)*/

const address = window.location.hostname;

let biometric_login = () => {
    const url = new URL(`${window.location.protocol}//${address}/passkeys/auth/begin`);

    const request = new Request(url, {
        method: 'GET',
    })

    fetch(request).then((response) => {
        return response.json().then((data) => {   
            data.publicKey.challenge = base64url.decode(data.publicKey.challenge);
            navigator.credentials.get(data)
            .then(credentialInfo => {

                fetch('/passkeys/auth/complete',{
                    method: 'POST',
                    headers: { 'Accept': 'application/json',
                            'X-Requested-With':'XMLHttpRequest',
                            'X-CSRFToken': csrftoken},
                    body: JSON.stringify(publicKeyCredentialToJSON(credentialInfo))
                }).then((response) => {
                    return response.json().then((data) => {
                        console.log(data);
                    })
                })
            })
            .catch(error => {
                alert('Authentication error:'+ error.message);
            });
        })
    })
}

PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable()
    .then((available) => {
        if (available) {
            var navbar = document.getElementById('navbar');
            if (navbar.hasAttribute('data-passkey')) {
                var button = document.createElement('button');
                button.innerHTML = '<i class = "fas fa-shield-alt"></i> biometric login';
                button.setAttribute('onclick','biometric_login()');

                document.getElementById('login').prepend(button);
            }
        }
    })