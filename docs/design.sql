START TRANSACTION;

DROP TABLE IF EXISTS Ticket;
DROP TABLE IF EXISTS Hacker;
DROP TABLE IF EXISTS TicketStatus;

CREATE TABLE Hacker (
    userId
        SERIAL PRIMARY KEY,
    userName
        varchar(50) NOT NULL,
    userEmail
        varchar(256) UNIQUE NOT NULL,
    userRegisterTime
        timestamp without time zone NOT NULL
        default (now() at time zone 'utc')
);

CREATE TABLE TicketStatus (
    ticketStatusId
        SERIAL PRIMARY KEY,
    ticketStatusName
        varchar(15) UNIQUE NOT NULL
);

CREATE TABLE Ticket (
    ticketId
        SERIAL PRIMARY KEY,
    userId
        int REFERENCES Hacker,
    ticketTableNumber
        int NOT NULL,
    ticketContents
        varchar(150) NOT NULL,
    ticketStatusId
        int REFERENCES ticketStatus NOT NULL,
    ticketCreationTime
        timestamp without time zone NOT NULL
        default (now() at time zone 'utc'),
    ticketMentorData
        varchar(500)
);

INSERT INTO TicketStatus ( ticketStatusName ) VALUES ( 'pending' );
INSERT INTO TicketStatus ( ticketStatusName ) VALUES ( 'confirmed' );
INSERT INTO TicketStatus ( ticketStatusName ) VALUES ( 'sent' );
INSERT INTO TicketStatus ( ticketStatusName ) VALUES ( 'closed' );

COMMIT;
