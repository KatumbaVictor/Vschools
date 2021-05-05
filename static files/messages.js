function send_message(){
    if (document.getElementById("message").value.length>0){
        fetch("http://127.0.0.1:8000/messages/",{
            method: "POST",
            body: document.getElementById("message").value,
            headers: {"X-Requested-With":"XMLHttpRequest"}
        }).then(function(){
            document.getElementById('divthree').innerHTML += 
            '<p class = "sender">'+document.getElementById("message").value+'</p>';
            document.getElementById("message").value = "";
        }
        )
    }
}