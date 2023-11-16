const username = document.getElementById('navbar').dataset.username;
const email = document.getElementById('navbar').dataset.email;
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

var address;

var challenge;
var user_id;

if (window.location.protocol == 'https:'){
    address = 'vschoolsmeet.tech'
}else {
    address = 'localhost:8000'
}

const create_credential = () => {
    var url = new URL(`${window.location.protocol}//${address}/webauthn-registration-options/`);

    const request = new Request(url, {
        method: 'GET',
    })

    fetch(request).then((response) => {
        return response.json().then((data) => {
            challenge = data.challenge;
            user_id = data.user_id;
            get_registration_options(JSON.parse(data));
        })
    })
}

const get_registration_options = (data) => {
    if (typeof navigator.credentials !== 'undefined') {
          data.challenge = new TextEncoder().encode(data.challenge).buffer;
          data.user.id = new TextEncoder().encode(data.user.id).buffer;
          delete data.rp.id

          var credential = {'publicKey':data};

          navigator.credentials.create(credential)
            .then(credentialInfo => {
              
              var url = new URL(`${window.location.protocol}//${address}/webauthn-verify-options/`);

              const request = new Request(url, {
                  method: 'POST',
                  body: credentialInfo,
                  headers: new Headers({
                      'X-CSRFToken': csrftoken,
                      'X-Requested-With': 'XMLHttpRequest'
                  }),
              })

              fetch(request).then((response) => {
                  return response.json().then((data) => {
                      console.log(data);
                  })
              })
            })
    }
}