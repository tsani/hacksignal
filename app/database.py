from app import app

import psycopg2

class Database:
    @staticmethod
    def get_connection():
        return psycopg2.connect(
                "dbname='%s' user='%s' password='%s' host='%s'" %
                tuple(app.config['DATABASE'][k]
                    for k in ['name', 'user', 'password', 'host']))

    @staticmethod
    def get_tickets(selector):
        conn = Database.get_connection()
        cur = conn.cursor()

        column_names = ['ticketId', 'ticketContents', 'ticketTableNumber',
                'ticketStatusName', 'userId', 'userName', 'userEmail']
        columns = ', '.join(column_names)

        if selector == "all":
            # then select all tickets
            cur.execute(
                    "SELECT " + columns + " FROM Ticket "
                    "NATURAL JOIN Hacker NATURAL JOIN TicketStatus;")
        elif selector == "open":
            # then select all non-closed tickets
            cur.execute(
                    "SELECT " + columns + " FROM Ticket "
                    "NATURAL JOIN Hacker "
                    "NATURAL JOIN TicketStatus "
                    "WHERE ticketStatusName!='closed';")
        else:
            # then try to look up the given selector
            cur.execute(
                    "SELECT * FROM TicketStatus WHERE ticketStatusName=%s;",
                    (ticket_type,))

            # if it does not exist
            if not cur.rowcount:
                raise ValueError(" no such ticket status '%s'." % selector)
                #return jsonify( {
                #    "status": "failed",
                #    "message": "no such ticket status '%s'." % ticket_type
                #} )

            # get the tickets of that kind
            cur.execute(
                    "SELECT " + columns + " FROM Ticket "
                    "NATURAL JOIN Hacker NATURAL JOIN TicketStatus "
                    "WHERE ticketStatusName!=%s;", (ticket_type,))

        records = [dict(zip(column_names, r)) for r in cur.fetchall()]
        conn.close()
        return records

    @staticmethod
    def create_user_if_not_exists(name, email):
        """ Returns the id of the user. Raises a ValueError if the user
            already exists and the names don't match! """
        conn = Database.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT userId, userName FROM Hacker WHERE userEmail=%s;",
                (email,))
        if not cur.rowcount: # if the user doesn't exist
            # create them
            cur.execute("INSERT INTO hacker ( userName, userEmail ) "
                    "VALUES ( %s, %s );",
                    (name, email))
            cur.execute("SELECT LASTVAL();")
            user_id = cur.fetchone()
            cur.execute("SELECT userId, userName FROM Hacker WHERE userId=%s;",
                    (user_id,))

            conn.commit()

        # fetch the record that was either selected or inserted
        record = cur.fetchone()
        # check that the names match
        if name != record[1]:
            raise ValueError("The given name '%s' does not match the one "
                    "already associated with that email address, '%s'." %
                    (name, record[1]))

        return record[0] # return the userId

    @staticmethod
    def create_ticket(user_id, ticket_table_number, ticket_contents,
            ticket_status_name):
        """ Create a ticket. """
        conn = Database.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT ticketStatusId FROM TicketStatus "
                "WHERE ticketStatusName=%s;",
                (ticket_status_name,))
        if not cur.rowcount:
            raise ValueError('invalid ticket status name')

        (ticket_status_id,) = cur.fetchone()
        cur.execute("INSERT INTO Ticket "
                "( userId, ticketTableNumber, ticketContents, ticketStatusId ) "
                "VALUES ( %s, %s, %s, %s ) RETURNING ticketId;",
                (user_id, ticket_table_number, ticket_contents,
                    ticket_status_id))
        conn.commit()
        (ticket_id,) = cur.fetchone()
        return ticket_id

    @staticmethod
    def update_ticket_status(ticket_id, ticket_status_name):
        conn = Database.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT ticketStatusId FROM TicketStatus "
                "WHERE ticketStatusName=%s;",
                (ticket_status_name,))
        if not cur.rowcount:
            raise ValueError("invalid ticket status name %s" %
                    (ticket_status_name,))
        (ticket_status_id,) = cur.fetchone()[0]
        cur.execute("UPDATE Ticket SET ( ticketStatusId ) = ( %s ) "
                "WHERE ticketId=%s;",
                (ticket_statis_id, ticket_id))
        conn.commit()

    @staticmethod
    def delete_ticket(ticket_id):
        with Database.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM Ticket WHERE ticketId=%s;", ticket_id)
