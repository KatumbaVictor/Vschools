function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
    

function save_post(evt){
    fetch('http://127.0.0.1:8000/home/',{
        method: "POST",
        headers: { 'Accept': 'application/json',
                    "X-CSRFToken": getCookie('csrftoken'),
                    'X-Requested-With':'XMLHttpRequest'},
        body: JSON.stringify({'save':evt.dataset.post_id})
    }).then(function(){
        evt.innerHTML = '<i class = "fas fa-bookmark"></i>';
    })
}

function like(evt){
    fetch('http://127.0.0.1:8000/home/',{
        method: "POST",
        headers: { 'Accept': 'application/json',
                    "X-CSRFToken": getCookie('csrftoken'),
                    'X-Requested-With':'XMLHttpRequest'},
        body: JSON.stringify({'like':evt.dataset.post_id})
    }).then(function(){
        evt.innerHTML = '<i class = "fas fa-heart"></i>';
    })
}


