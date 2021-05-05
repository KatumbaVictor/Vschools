navigator.mediaDevices.getUserMedia({video: true})
.then(function(stream){
    document.getElementById('vid').srcObject = stream;
    const videos = document.getElementsByClassName('video2');
    for(let i = 0; videos.length; i++){
        videos[i].srcObject = stream;
    }
}) 