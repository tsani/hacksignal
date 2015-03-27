from app import app, socketio
from app.database import Database

from flask import jsonify, request

from app.auth import requires_auth

@app.route('/api/tickets/list/<ticket_type>')
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
    records = Database.list_tickets(ticket_type)

    return jsonify( {
        "records": records,
        "status": "ok",
    } )

@app.route('/api/tickets/get/<ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    return jsonify(Database.get_ticket(ticket_id))

@app.route('/api/tickets/modify/<ticket_id>', methods=['POST'])
@requires_auth
def modify_ticket(ticket_id):
    did_something = False
    request_data = request.get_json(force=True)

    if 'ticketStatusName' in request_data:
        did_something = True
        try:
            Database.update_ticket_status(
                    ticket_id, request_data['ticketStatusName'])
        except ValueError as e:
            return jsonify( {
                "status": "failed",
                "message": "could not update ticket status: " + str(e)
            })

    if 'ticketMentorData' in request_data:
        did_something = True
        Database.update_ticket_data(
                ticket_id, request_data['ticketMentorData'])

    if not did_something:
        return jsonify( {
            "status": "failed",
            "message": "supply one of ticketStatusName or ticketMentorData"
                        " to modify."
        })

    return jsonify( {
        "status": "ok",
    })

@app.route('/api/ticketstatus/list', methods=['GET'])
def ticket_status_list():
    names = Database.get_ticket_status_names()
    return jsonify( {
        "status": "ok",
        "ticketStatusNames": names
    })

@app.route('/api/tickets/delete/<ticket_id>', methods=['POST'])
@requires_auth
def delete_ticket(ticket_id):
    try:
        Database.delete_ticket(ticket_id)
    except Exception as e:
        return jsonify( {
            "status": "failed",
            "message": str(e)
        })
    else:
        socketio.emit('delete ticket', {
            'ticketId': ticket_id
        }, room='__admin__', namespace='/chat')

        return jsonify( {
            "status": "ok"
        })

@app.route('/api/users/delete', methods=['POST'])
@requires_auth
def delete_user():
    request_data = request.get_json()

    if 'userEmail' in request_data:
        Database.delete_user(user_email=request_data['userEmail'])
    elif 'userId' in request_data:
        Database.delete_user(user_id=request_data['userId'])
    else:
        return jsonify( {
            "status": "failed",
            "message": "you need to specify either the userEmail or userId"
        })

    return jsonify( {
        "status": "ok",
    })
