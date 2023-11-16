const address = window.location.hostname;
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const UserID = document.getElementById('navbar').dataset.id;
const form = new FormData();

let authenticate = () => {
    fetch('/webauthn-authentication-options/',{
        method: 'GET'
    }).then((response) => {
        return response.json().then((data) => { 
            console.log(data)
            data.publicKey.challenge = base64url.decode(data.publicKey.challenge);

            navigator.credentials.get(data)
            .then(credentialInfo => {
                console.log(credentialInfo)

                var item = {'credential':publicKeyCredentialToJSON(credentialInfo), 
                            'challenge':credentialInfo.challenge, 'rpId':credentialInfo.rpId,
                            'origin':address}

                form.append('passkeys', JSON.stringify(publicKeyCredentialToJSON(credentialInfo)))

                fetch('/webauthn-authenticate/',{
                    method: 'POST',
                    headers: {'X-Requested-With':'XMLHttpRequest',
                              'X-CSRFToken': csrftoken,
                              },
                    body: form
                }).then((response) => {
                    return response.json().then((data) => {
                        console.log(data);
                    })
                })
            })
            .catch(error => {
                console.error('Authentication error:'+ error.message);
            });
        })
    })
}

PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable()
    .then((available) => {
        if (available) {
            console.log('available')
        }
    })