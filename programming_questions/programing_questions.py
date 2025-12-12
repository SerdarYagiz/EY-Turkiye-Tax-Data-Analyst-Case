from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, joinedload
from sqlalchemy.exc import SQLAlchemyError

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "mydb",
    "user": "admin",
    "password": "secret123"
}

DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

Base = declarative_base()

engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=False, max_overflow=10)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ORM MODELS
class Team(Base):
    __tablename__ = 'teams'

    team_id = Column(Integer, primary_key=True, autoincrement=True)
    team_name = Column(String(100), nullable=False)

    tickets = relationship('Ticket', back_populates='team')

    def __repr__(self):
        return f"<Team(id={self.team_id}, name='{self.team_name}')>"


class Client(Base):
    __tablename__ = 'clients'

    client_id = Column(Integer, primary_key=True, autoincrement=True)
    client_name = Column(String(200), nullable=False)

    tickets = relationship('Ticket', back_populates='client')

    def __repr__(self):
        return f"<Client(id={self.client_id}, name='{self.client_name}')>"


class Ticket(Base):
    __tablename__ = 'tickets'

    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey('teams.team_id'), nullable=False)
    ticket_date = Column(Date, nullable=False)
    resolution_date = Column(Date, nullable=True)
    client_id = Column(Integer, ForeignKey('clients.client_id'), nullable=False)

    team = relationship('Team', back_populates='tickets')
    client = relationship('Client', back_populates='tickets')

    def __repr__(self):
        return f"<Ticket(id={self.ticket_id}, team={self.team_id}, date={self.ticket_date})>"

    @property
    def resolution_days(self) -> Optional[int]:
        if self.resolution_date:
            return (self.resolution_date - self.ticket_date).days
        return None


# QUESTION 1
# Connect to database, retrieve tickets, handle errors
def fetch_tickets_from_db() -> List[Dict]:
    session = None
    tickets = []

    try:
        session = SessionLocal()

        ticket_objects = session.query(Ticket)\
            .options(joinedload(Ticket.team))\
            .options(joinedload(Ticket.client))\
            .all()

        # Convert to dictionaries
        for ticket in ticket_objects:
            tickets.append({
                "ticket_id": ticket.ticket_id,
                "team": ticket.team.team_name,
                "ticket_date": ticket.ticket_date.strftime("%Y-%m-%d"),
                "resolution_date": ticket.resolution_date.strftime("%Y-%m-%d") if ticket.resolution_date else None,
                "client_id": ticket.client_id
            })

        return tickets

    except SQLAlchemyError as e:
        print(f"Database connection error: {e}")
        return []

    finally:
        if session:
            session.close()
            print("Database connection closed.")


# QUESTION 2
# Count tickets opened by each team
def count_tickets_by_team(tickets: List[Dict]) -> Dict[str, int]:
    team_counts = {}

    for ticket in tickets:
        team = ticket.get("team")
        if team:
            team_counts[team] = team_counts.get(team, 0) + 1

    return team_counts


# QUESTION 3
# Filter tickets resolved within given days
def tickets_resolved_within_days(tickets: List[Dict], max_days: int) -> List[Dict]:
    result = []

    for ticket in tickets:
        ticket_date = ticket.get("ticket_date")
        resolution_date = ticket.get("resolution_date")

        if not ticket_date or not resolution_date:
            continue

        try:
            opened = datetime.strptime(ticket_date, "%Y-%m-%d")
            resolved = datetime.strptime(resolution_date, "%Y-%m-%d")
        except ValueError:
            continue

        if (resolved - opened).days <= max_days:
            result.append(ticket)

    return result


if __name__ == "__main__":
    print("\n Question 1: Fetching tickets from database...")
    tickets = fetch_tickets_from_db()
    print(f"Total tickets fetched: {len(tickets)}")

    print("\n Question 2: Ticket count by team")
    team_counts = count_tickets_by_team(tickets)
    for team, count in team_counts.items():
        print(f"{team}: {count}")

    print("\n Question 3: Tickets resolved within 7 days")
    fast_resolved = tickets_resolved_within_days(tickets, 7)
    print(f"Tickets resolved within 7 days: {len(fast_resolved)}")

    for ticket in fast_resolved:
        print(ticket)