from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Table

Base = declarative_base()

attendee_event = Table('attendee_event', Base.metadata,
    Column('attendee_id', Integer, ForeignKey('attendees.id'), primary_key=True),
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True)
)

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    date = Column(Date, nullable=False)
    location = Column(String)
    tickets = relationship('Ticket', back_populates='event')
    attendees = relationship('Attendee', secondary=attendee_event, back_populates='events')

class Attendee(Base):
    __tablename__ = 'attendees'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    phone = Column(String)
    events = relationship('Event', secondary=attendee_event, back_populates='attendees')

class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    available_quantity = Column(Integer, default=0)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    event = relationship('Event', back_populates='tickets')
