var socket = io.connect('/chat');

$(document).ready(function(){
    socket.emit('auth', {
        username: token // a global variable provided by chat.html
    });
});

function scrollToBottom() {
    var box    = $('.chatlog');
    var height = box[0].scrollHeight;
    box.scrollTop(height);
}

function sendChatMessage() {
    socket.emit('chat message', {
        sender: token,
        data: $('#msg-content').val()
    });
    return false;
}

socket.on('server message', function(msg) {
    $('.chatlog').append(
        '<p class="server-message"><span class="label-bold">Mr. Web Server: </span>' + msg.data + '</p>');
});

socket.on('chat message', function(msg) {
    $('.chatlog').append(
        '<p class="message"><span class="label-bold">' +
        'You:</span> ' +
        msg.data +
        '</p>'
    );

    // if we got the bounce-back from our own message, then our message was
    // sent successfully and we can clear the chatbox.
    if(msg.sender === token) {
        $('#msg-content').val('');
    }

    scrollToBottom();
});

socket.on('admin message', function(msg) {
    $('.chatlog').append(
        '<p class="admin-message"><span class="label-bold">' +
        msg.sender +
        ':</span> ' +
        msg.data +
        '</p>'
    );
    scrollToBottom();
});
