function getImage(){
    document.getElementById('image').click()
}

function getVideo(){
    document.getElementById('video').click()
}

function view_files(){
    const reader = new FileReader();
    reader.onload = function(){
        console.log(reader);
        document.getElementById('divtwo').style.display = "none";
        document.getElementById('img').src = reader.result;
        

    }
    reader.readAsDataURL(document.getElementById('image').files[0]);
}
