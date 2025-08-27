from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from . import Base, get_session
from datetime import datetime
from sqlalchemy.orm import relationship, joinedload

class Ticket(Base):
    __tablename__ = 'tickets'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    attendee_id = Column(Integer, ForeignKey('attendees.id'), nullable=False)
    booked_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    event = relationship("Event", back_populates="tickets")
    attendee = relationship("Attendee", back_populates="tickets")
    
    def __repr__(self):
        return f"<Ticket(id={self.id}, event_id={self.event_id}, attendee_id={self.attendee_id}, booked_at={self.booked_at})>"
    
    # ORM Methods
    @classmethod
    def create(cls, event_id, attendee_id):
        """Create a new ticket"""
        session = get_session()
        try:
            # Check if event exists and has capacity
            from .event import Event
            event = session.query(Event).filter(Event.id == event_id).first()
            if not event:
                raise ValueError("Event not found")
            
            # Check if event is full
            current_tickets = session.query(cls).filter(cls.event_id == event_id).count()
            if current_tickets >= event.capacity:
                raise ValueError("Event is at full capacity")
            
            # Check if attendee exists
            from .attendee import Attendee
            attendee = session.query(Attendee).filter(Attendee.id == attendee_id).first()
            if not attendee:
                raise ValueError("Attendee not found")
            
            # Check if attendee already has ticket for this event
            existing_ticket = session.query(cls).filter(
                cls.event_id == event_id, 
                cls.attendee_id == attendee_id
            ).first()
            if existing_ticket:
                raise ValueError("Attendee already has a ticket for this event")
            
            ticket = cls(event_id=event_id, attendee_id=attendee_id)
            session.add(ticket)
            session.commit()
            session.refresh(ticket)
            return ticket
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @classmethod
    def get_all(cls):
        """Get all tickets"""
        session = get_session()
        try:
            return session.query(cls).all()
        finally:
            session.close()
    
    @classmethod
    def find_by_id(cls, ticket_id):
        """Find ticket by ID"""
        session = get_session()
        try:
          from sqlalchemy.orm import joinedload
          return session.query(cls).options(
              joinedload(cls.event),
              joinedload(cls.attendee)
           ).filter(cls.id == ticket_id).first()   
        finally:
            session.close()
    
    @classmethod
    def find_by_event_and_attendee(cls, event_id, attendee_id):
        """Find ticket by event and attendee"""
        session = get_session()
        try:
            return session.query(cls).filter(
                cls.event_id == event_id,
                cls.attendee_id == attendee_id
            ).first()
        finally:
            session.close()
    
    @classmethod
    def get_tickets_for_event(cls, event_id):
        """Get all tickets for a specific event"""
        session = get_session()
        try:
           from sqlalchemy.orm import joinedload
           return session.query(cls).options(
             joinedload(cls.attendee)
           ).filter(cls.event_id == event_id).all()
        finally:
            session.close()
    
    @classmethod
    def get_tickets_for_attendee(cls, attendee_id):
        """Get all tickets for a specific attendee"""
        session = get_session()
        try:
            return session.query(cls).filter(cls.attendee_id == attendee_id).all()
        finally:
            session.close()
    
    def delete(self):
        """Delete this ticket (cancel booking)"""
        session = get_session()
        try:
            session.delete(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_event_details(self):
        """Get event details for this ticket"""
        return self.event
    
    def get_attendee_details(self):
        """Get attendee details for this ticket"""
        return self.attendee