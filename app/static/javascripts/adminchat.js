var socket = io.connect(
    'http://' + document.domain + ':' + location.port + '/chat');

console.log('connected');

function sendAdminMessage(ticketId) {
    var ticketLi = document.getElementById('ticket-list-item-' + ticketId);
    var user = $(ticketLi).find('.tl-email').text().trim();
    var msgContent = $(ticketLi).find('option:selected').val();
    socket.emit('admin message', {
        data: msgContent,
        password: password, //ayyyy lmao
        destination: user
    });

    return false;
}

socket.on('server message', function(msg) {
    console.log(JSON.stringify(msg));
});

$(document).ready(function(){
    socket.on('error message', function(msg) {
        console.log(msg);
    });
});
