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
            ticketMentorData = $.trim(
                    $("#ticket-list-item-" + ticketId + " > textarea")
                    .val())
            console.log(ticketStatusName, ticketMentorData);
            $.post('/api/tickets/modify/' + ticketId, JSON.stringify({
                ticketStatusName: ticketStatusName,
                ticketMentorData: ticketMentorData
            }), function(response) {
                console.log(response.status);
                location.reload();
            }, 'json');
        }
    }
})();
