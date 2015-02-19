from app import app
from app.database import Database

from flask import jsonify, request

from app.auth import requires_auth

@app.route('/api/tickets/get/<ticket_type>')
def get_tickets(ticket_type):
    """ Fetch tickets of the given type from the database
        Ticket types are:
            * 'sent': ticket has been opened, but no action has been taken
            * 'pending': ticket has been reviewed by mentorship admins
            * 'confirmed': a mentor has been found and dispatched
            * 'closed': the mentor has visited the requester

        Two special types are provided for convenience:
            * 'all': get all the tickets, regardless of type
            * 'open': get all non-closed tickets.

        The returned JSON blob has the following format:
        {
            "records": [ /* array of the matched records */ ],
            "status": "ok" or "failed",
            "message": "a message describing the failure, if any"
        }

        The `message` field is absent if the `status` is "ok", and the `records`
        field is absent if the `status` is "failed". In other words, always
        check the status field.
    """
    conn = Database.get_connection()
    cur = conn.cursor()

    # make the database output look like nice JSON
    records = Database.get_tickets(ticket_type)

    return jsonify( {
        "records": records,
        "status": "ok",
    } )

@app.route('/api/tickets/modify/<id>', methods=['POST'])
@requires_auth
def modify_ticket(ticket_id):
    request_data = request.get_json()

    if 'ticketStatusName' not in request_data:
        return jsonify( {
            "status": "failed",
            "message": "no new ticket status given"
        })

    try:
        Database.update_ticket_status(
                ticket_id, request_data['ticketstatusname'])
    except ValueError as e:
        return jsonify( {
            "status": "failed",
            "message": str(e)
        })

    return jsonify( {
        "status": "ok",
    })
