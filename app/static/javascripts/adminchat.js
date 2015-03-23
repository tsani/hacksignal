var socket = io.connect(
    'http://' + document.domain + ':' + location.port + '/chat');

console.log('connected');

function sendAdminMessage(user, message) {
    user = 'sample-token';
    socket.emit('admin message', {
        data: message,
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
