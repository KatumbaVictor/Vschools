function getImage(){
    document.getElementById('image').click()
}

function getVideo(){
    document.getElementById('video').click()
}

function view_files(){
    var reader = new FileReader();
    reader.onload = function(){
        console.log(reader.result);
    }
}
