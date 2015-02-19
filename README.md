McHacks Mentorship Platform
===========================

The one-of-a-kind unique and amazing McHacks mentor dispatching service !

API
=====

1. `/api/tickets/get/<status>` (GET)

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

2. `/api/tickets/modify/<id>` (POST)

    Change the given ticket's status.

    POST a JSON blob of the following form to this endpoint to set the
    identified ticket's status.

        {
            "ticketStatusName": "pending" / "closed" / etc.
        }

    Note: this endpoint requires HTTP basic authentication.

3. `/api/tickets/delete/<id>` (POST)

    Delete the given ticket.

    The body of the request should be empty.

    Note: this endpoint requires HTTP basic authentication.
