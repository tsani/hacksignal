from app import app
from app.database import Database

from flask import jsonify

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

    if ticket_type == "all":
        cur.execute(
                "SELECT * FROM Ticket "
                "NATURAL JOIN Hacker "
                "NATURAL JOIN TicketStatus;")
    elif ticket_type == "open":
        cur.execute(
                "SELECT * FROM Ticket "
                "NATURAL JOIN Hacker "
                "NATURAL JOIN TicketStatus "
                "WHERE ticketStatusName!='closed';")
    else:
        cur.execute(
                "SELECT * FROM TicketStatus WHERE ticketStatusName=%s;",
                (ticket_type,))

        if not cur.rowcount:
            return jsonify( {
                "status": "failed",
                "message": "no such ticket status '%s'." % ticket_type
            } )

        cur.execute(
                "SELECT * FROM Ticket NATURAL JOIN Hacker NATURAL JOIN TicketStatus "
                "WHERE ticketStatusName!=%s;", (ticket_type,))

    # make the database output look like nice JSON
    records = []
    while True:
        r = cur.fetchone()
        if r is None:
            break
        d = dict(zip([d.name for d in cur.description], r))
        records.append(d)

    return jsonify( {
        "records": records,
        "status": "ok",
    } )
