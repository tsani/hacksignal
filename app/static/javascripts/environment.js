mentorship = (function() {
    return {
        sendDeleteTicket: function(ticketId) {
            $.post('/api/tickets/delete/' + ticketId, {}, function(response) {
                console.log(response.status, response.message);
                location.reload();
            });
        }
    }
})();
