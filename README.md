McHacks Mentorship Platform
===========================

The one-of-a-kind unique and amazing McHacks mentor dispatching service !

Setup
=====

To set up the package, you'll need a recent version of PostgreSQL, and python 3.

1. Creating the database.

    Open the PostgreSQL REPL and create the mchacks user and database.

        $ psql -U postgres

        postgres=# CREATE USER mchacks;
        CREATE USER
        postgres=# CREATE DATABASE mchacks;
        CREATE DATABASE
        postgres=# \q

    Then, load the schema.

        $ psql -U mchacks < docs/design.sql

2. The Python virtual environment.

    Set up a python 3 virtualenv called `venv`, activate it, and install the
    required packages.

        $ virtualenv venv --python=/usr/bin/path/to/your/python3/interpreter
        $ source venv/bin/activate
        (venv) $ pip install -r requirements.txt

3. Tell us your secrets.

    You need to write a small configuration module called `secret_config.py`
    in the project root. Its contents should look something like the following.

        DATABASE = {
                "user": "mchacks",
                "password": "seeeeekret",
                "name": "mchacks",
                "host": "localhost",
                "active": True
        }

        AUTHENTICATION = {
                "username": "1337hacker",
                "password": "sup3rs3cr3t"
        }

        SECRET_KEY = "annoy-everyone-with-this-one-weird-trick"

    The `AUTHENTICATION` dictionary is used for the HTTP basic auth implemented
    for the administration panel.

    The `active` key in the `DATABASE` dictionary is used to determine whether
    a real database connection should be used (as specified in the `DATABASE`
    dictionary), or whether a dummy database should be used.

3. Running the server.

    To run the server, we deploy it with Gunicorn, which will have been
    installed to your virtualenv by pip. A script `gunicorn.sh` is provided for
    your convenience. If you get a failed to bind error message, change the
    port in `gunicorn.sh`. You can also configure Gunicorn settings in there.

        $ ./gunicorn.sh


And there you go!


API
=====

1. `/api/tickets/list/<status>` (GET)

    Fetch tickets of the given type from the database

    Ticket types are:
     * `sent`: ticket has been opened, but no action has been taken
     * `pending`: ticket has been reviewed by mentorship admins
     * `confirmed`: a mentor has been found and dispatched
     * `closed`: the mentor has visited the requester

    Two special types are provided for convenience:
     * `all`: get all the tickets, regardless of type
     * `open`: get all non-closed tickets.

    The returned JSON blob has the following format:

        {
            "records": [ /* array of the matched records */ ],
            "status": "ok" or "failed",
            "message": "a message describing the failure, if any"
        }

    The `message` field is absent if the `status` is "ok", and the `records`
    field is absent if the `status` is "failed". In other words, always
    check the status field.

    Each ticket record has the following format:

        {
            "ticketId": N,
            "ticketContents": "a string",
            "ticketTableNumber": M,
            "ticketStatusName": "the status of the ticket",
            "userId": P,
            "userName": "the username of the submitter",
            "userEmail": "theiremail@somehost.website"
        }

2. `/api/tickets/get/<id>` (GET)

    Get details on the identified ticket.

    The result is a single ticket record in the format described in
    `/api/tickets/list/<status>`.

3. `/api/tickets/modify/<id>` (POST)

    Change the given ticket's status.

    POST a JSON blob of the following form to this endpoint to set the
    identified ticket's status.

        {
            "ticketStatusName": "pending" / "closed" / etc.
        }

    Note: this endpoint requires HTTP basic authentication.

4. `/api/tickets/delete/<id>` (POST)

    Delete the given ticket.

    The body of the request should be empty.

    Note: this endpoint requires HTTP basic authentication.

5. `/api/users/delete` (POST)

    Delete the user identified by the criterion given in the request body.

    The request body should be JSON representing an object of the following
    form.

        {
            "userEmail": "email@address.com"
        }

    or

        {
            "userId": 123
        }

    The rationale for allowing both ids and emails is that both are unique.

    Note: this also deletes all the tickets owned by the user.

    Note: this endpoint requires HTTP basic authentication.
