START TRANSACTION;

DROP TABLE IF EXISTS Hacker;
DROP TABLE IF EXISTS TicketStatus;
DROP TABLE IF EXISTS Ticket;

CREATE TABLE Hacker (
    userId int PRIMARY KEY,
    userName varchar(50),
    userEmail varchar(256) UNIQUE
);

CREATE TABLE TicketStatus (
    ticketStatusId SERIAL PRIMARY KEY,
    ticketStatusName varchar(15) UNIQUE
);

CREATE TABLE Ticket (
    ticketId SERIAL PRIMARY KEY,
    userId int REFERENCES Hacker,
    ticketContents varchar(150),
    ticketStatusId int REFERENCES ticketStatus
);

INSERT INTO Hacker ( userId, userName, userEmail ) VALUES ( 0, 'null', 'no email' );

INSERT INTO TicketStatus ( ticketStatusId, ticketStatusName ) VALUES ( 0, 'no ticket' );

INSERT INTO TicketStatus ( ticketStatusName ) VALUES ( 'sent' );
INSERT INTO TicketStatus ( ticketStatusName ) VALUES ( 'pending' );
INSERT INTO TicketStatus ( ticketStatusName ) VALUES ( 'confirmed' );
INSERT INTO TicketStatus ( ticketStatusName ) VALUES ( 'closed' );

INSERT INTO Ticket ( ticketId, userId, ticketContents, ticketStatusId ) VALUES ( 0, 0, 'empty ticket', 0 );

COMMIT;
