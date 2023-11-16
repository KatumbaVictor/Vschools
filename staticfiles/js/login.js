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

var address;

if (window.location.protocol == 'https:'){
    address = 'vschoolsmeet.tech'
}else {
    address = 'localhost:8000'
}

let biometric_login = () => {
    const url = new URL(`${window.location.protocol}//${address}/webauthn-authentication-options/`);

    const request = new Request(url, {
        method: 'GET',
    })

    fetch(request).then((response) => {
        return response.json().then((data) => {                
            navigator.credentials.get({ publicKey: response })
            .then(credentialInfo => {
                const authentication_url = new URL(`${window.location.protocol}//${address}/webauthn-authenticate/`);

                const authentication_request = new Request(authentication_url, {
                    method: 'POST',
                    body: credentialInfo,
                    headers: new Headers({
                        'X-CSRFToken': csrftoken,
                        'X-Requested-With': 'XMLHttpRequest'
                    }),
                })

                fetch(authentication_request).then((response) => {
                    return response.json().then((data) => {
                        console.log(data);
                    })
                })
            })
            .catch(error => {
                console.error('Authentication error:', error);
            });
        })
    })
}