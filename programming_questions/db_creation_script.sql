CREATE TABLE teams (
    team_id INT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL
);

CREATE TABLE clients (
    client_id INT PRIMARY KEY,
    client_name VARCHAR(150) NOT NULL
);

CREATE TABLE tickets (
    ticket_id INT PRIMARY KEY,
    team_id INT NOT NULL,
    ticket_date DATE NOT NULL,
    resolution_date DATE,
    client_id INT NOT NULL,

    CONSTRAINT fk_team
        FOREIGN KEY (team_id) REFERENCES teams(team_id),

    CONSTRAINT fk_client
        FOREIGN KEY (client_id) REFERENCES clients(client_id)
);

CREATE INDEX idx_tickets_team_id ON tickets(team_id);
CREATE INDEX idx_tickets_ticket_date ON tickets(ticket_date);