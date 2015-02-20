mentorship = (function() {
    ticketStatusNames = []

    $.get('/api/ticketstatus/list', {}, function(response) {
        ticketStatusNames = response
    }, 'json');

    return {
        ticketStatusNames: function() {
            return ticketStatusNames;
        },
        sendDeleteTicket: function(ticketId) {
            $.post('/api/tickets/delete/' + ticketId, {}, function(response) {
                console.log(response.status, response.message);
                location.reload();
            }, 'json');
        },
        sendModifyTicket: function(ticketId) {
            ticketStatusName = $.trim(
                $("#ticket-list-item-" + ticketId + " > select")
                .find(":selected").text());
            console.log(ticketStatusName);
            $.post('/api/tickets/modify/' + ticketId, JSON.stringify({
                ticketStatusName: ticketStatusName
            }), function(response) {
                console.log(response.status);
                location.reload();
            }, 'json');
        }
    }
})();
