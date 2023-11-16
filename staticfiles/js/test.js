//Check if the WebAuthn API is supported by the browser
/*const registrationOptions = {
    'challenge': '',
    'rp': {
      'name': 'Vschools Meet'
    },

    'user': {
       'id':'id',
       'name': 'victor',
       'displayName': 'victor'
    },

    'pubKeyCredParams': [
      {'type': 'public-key', 'alg': -7},
      {'type': 'public-key', 'alg': -257}
    ]
};

if (window.PublicKeyCredential) {
   navigator.credentials.create({publicKey: registrationOptions})
   .then(credential => {
      const credentialResponse = credential.response;

      const registrationData = {
         id: credential.id,
         rawId: arrayBufferToBase64Url(credential.rawId),
         type: credential.type,
         response: {
            attestationObject: arrayBufferToBase64Url(credentialResponse.attestation),
            clientDataJSON: arrayBufferToBase64Url(credentialResponse.clientDataJSON)
         }
      }

      fetch('/register/', {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json'
         },
         body: JSON.stringify(registrationData)
      }).then(response => {

      })
   })
}*/

fetch('/auth/',{
        method: 'GET'
}).then(response => {
  
})