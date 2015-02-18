from app import app
from app.database import Database

from flask import jsonify


@app.route('/api/tickets/get/<ticket_type>')
def get_tickets(ticket_type):
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
                "WHERE ticketStatusName!=%s;", ticket_type)

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

