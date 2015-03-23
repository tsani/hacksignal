$(document).ready(function(){
    var socket = io.connect(
        'http://' + document.domain + ':' + location.port + '/chat');

    socket.emit('auth', {
        username: token // a global variable provided by chat.html
    });

    socket.on('server message', function(msg) {
        $('#chatlog').append(
            '<p class="server-message"><span class="author">Mr. Web Server: </span>' + msg.data + '</p>');
    });

    socket.on('chat message', function(msg) {
        $('#chatlog').append(
            '<p class="message"><span class="author">' +
            msg.sender +
            ':</span> ' +
            msg.data +
            '</p>'
        );
        scrollToBottom();
    });

    socket.on('admin message', function(msg) {
        $('#chatlog').append(
            '<p class="admin-message"><span class="author">' +
            msg.sender +
            ':</span> ' +
            msg.data +
            '</p>'
        );
        scrollToBottom();
    });

    console.log('registered socket event handler');

    $('#chatinput').submit(function(event) {
        socket.emit('chat message', {
            sender: token,
            data: $('#msg-content').val()
        });
        $("#msg-content").val("");
        return false;
    });

    console.log('registered click event handler');
});

function scrollToBottom() {
    var box    = $('#chatlog');
    var height = box[0].scrollHeight;
    box.scrollTop(height);
}
