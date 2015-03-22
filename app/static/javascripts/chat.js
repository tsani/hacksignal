$(document).ready(function(){
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    socket.on('my response', function(msg) {
        $('#chatlog').append('<p>Received: ' + msg.data + '</p>');
    });
    $('form#chatinput').submit(function(event) {
        socket.emit('my event', {data: $('#msg-content').val()});
        return false;
    });
});