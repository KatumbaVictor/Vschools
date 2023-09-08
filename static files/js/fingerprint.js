const username = document.getElementById('navbar').dataset.username;
const email = document.getElementById('navbar').dataset.email;
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

const create_credential = () => {
    // Check for WebAuthn API support
    if (typeof navigator.credentials !== 'undefined') {
          // Create a new credential
          const credential = {
              publicKey: {
                rp: { name: 'Vschools dialogue.' },
                user: {
                  id: new Uint8Array(16),
                  name: email,
                  displayName: username,
                },
                pubKeyCredParams: [
                  {type: 'public-key', alg: -7},  // ES256
                  {type: 'public-key', alg: -257} // RS256
                ],
                attestation: 'direct',
                authenticatorSelection: {userVerification: 'required'},
                timeout: 60000,
                challenge: new Uint8Array(32),
              },
          };

          navigator.credentials.create(credential)
            .then(credentialInfo => {
              // Send attestation response to server for registration
              console.log(credentialInfo);
              var clientDataJSON = credentialInfo.response.clientDataJSON;
              var attestationObject = credentialInfo.response.attestationObject;

              var data = {'clientDataJSON':clientDataJSON, 'attestationObject':attestationObject};

              fetch(window.location,{
                method: 'POST',
                headers:{
                    'Content-Type': 'application/json',
                    'X-Requested-With':'XMLHttpRequest',
                    "X-CSRFToken": csrftoken
                },
                body: JSON.stringify(data)
                })
            })
            .catch(error => {
              console.error('Credential creation error:', error);
            });

      /*
      // Authenticating a user
      const assertion = {
        publicKey: {
          challenge: new Uint8Array(32),
          allowCredentials: [
            {
              id: new Uint8Array(16),
              type: 'public-key',
            },
          ],
        },
      };

      navigator.credentials.get({ publicKey: assertion })
        .then(credentialInfo => {
          // Verify the assertion on the server
        })
        .catch(error => {
          console.error('Authentication error:', error);
        });*/
    }
}

const url = new URL('http://localhost:8000/webauthn/signup_request/');

const request = new Request(url, {
    method: 'POST',
    body: JSON.stringify({'username':username, 'display_name': email}),
    headers: new Headers({
        'Content-Type':'application/json',
        'Accept':'application/json'
        /*'X-CSRFToken': csrftoken,
        'X-Requested-With': 'XMLHttpRequest'*/
    }),
})

fetch(request).then((response) => {
    return response.json().then((data) => {
        console.log(data);
    })
})