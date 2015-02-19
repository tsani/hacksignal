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
