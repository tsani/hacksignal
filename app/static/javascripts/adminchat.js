var socket = io.connect(
    'http://' + document.domain + ':' + location.port + '/chat');

console.log('connected');

function alertDispatched(email) {
    //var user = email;
    var user = 'sample-token';

    socket.emit('admin message', {
        data: 'Your mentor has been dispatched.',
        password: password, //ayyyy lmao
        destination: user
    });
    return false;
}

function alertNP(email) {
    //var user = email;
    var user = 'sample-token';

    socket.emit('admin message', {
        data: 'No problem, fake user!',
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
