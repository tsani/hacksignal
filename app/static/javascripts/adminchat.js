var socket = io.connect(
    'http://' + document.domain + ':' + location.port + '/chat');

console.log('connected');

function sendAdminMessage(user) {
    user = 'sample-token';
    msgContent = $("#responseOptions").val();
    socket.emit('admin message', {
        data: msgContent,
        password: password, //ayyyy lmao
        destination: user
    });
    return false;
}

$(document).ready(function(){
    socket.on('error message', function(msg) {
        console.log(msg);
    });
});

$("#responseOptions").change(function() {
    var msgContent = "";
    msgContent = $("select option:selected").val();
});
