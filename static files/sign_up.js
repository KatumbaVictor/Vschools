let conn = new WebSocket("ws://127.0.0.1:8000/messages");

conn.onopen = function(){
    console.log('connection opened');
}

