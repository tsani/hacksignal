var socket = io.connect(
    'http://' + document.domain + ':' + location.port + '/chat');

console.log('connected');

function alertDispatched(email) {
    //var user = email;
    console.log('got into alertDispatched');
    var user = 'sample-token';

    socket.emit('admin message', {
        data: 'Your mentor has been dispatched.',
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
