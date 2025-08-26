from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from . import Base, get_session
import re

class Attendee(Base):
    __tablename__ = 'attendees'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    contact = Column(String, nullable=False)
    
    # Relationship to tickets
    tickets = relationship("Ticket", back_populates="attendee", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Attendee(id={self.id}, name='{self.name}', contact='{self.contact}')>"
    
    # Property methods
    # Ensures attendee names are not-empty, ≤100 characters, and only contain letters, spaces, hyphens, and apostrophes
    @property
    def name_property(self):
        return self._name
    
    @name_property.setter
    def name_property(self, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Attendee name cannot be empty")
        if len(value) > 100:
            raise ValueError("Attendee name cannot exceed 100 characters")
        # Check for valid name format (letters, spaces, hyphens only)
        if not re.match(r'^[a-zA-Z\s\-\']+$', value.strip()):
            raise ValueError("Name can only contain letters, spaces, hyphens, and apostrophes")
        self._name = value.strip()
    
    # validates that the contact is a proper email or phone number
    @property
    def contact_property(self):
        return self._contact
    
    @contact_property.setter
    def contact_property(self, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Contact information cannot be empty")
        
        # Basic email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        # Basic phone validation (simple format)
        phone_pattern = r'^[\+]?[0-9\s\-\(\)]{10,15}$'
        
        contact_clean = value.strip()
        if not (re.match(email_pattern, contact_clean) or re.match(phone_pattern, contact_clean)):
            raise ValueError("Contact must be a valid email address or phone number")
        
        self._contact = contact_clean
    
    # ORM Methods
    @classmethod
    def create(cls, name, contact):
        """Create a new attendee"""
        session = get_session()
        try:
            attendee = cls(name=name, contact=contact)
            session.add(attendee)
            session.commit()
            session.refresh(attendee)
            return attendee
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @classmethod
    def get_all(cls):
        """Get all attendees"""
        session = get_session()
        try:
            return session.query(cls).all()
        finally:
            session.close()
    
    @classmethod
    def find_by_id(cls, attendee_id):
        """Find attendee by ID"""
        session = get_session()
        try:
            return session.query(cls).filter(cls.id == attendee_id).first()
        finally:
            session.close()
    
    @classmethod
    def find_by_contact(cls, contact):
        """Find attendee by contact information"""
        session = get_session()
        try:
            return session.query(cls).filter(cls.contact == contact).first()
        finally:
            session.close()
    
    def delete(self):
        """Delete this attendee"""
        session = get_session()
        try:
            session.delete(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_events(self):
        """Get all events this attendee is registered for"""
        session = get_session()
        try:
            from .event import Event
            return session.query(Event).join(Event.tickets).filter_by(attendee_id=self.id).all()
        finally:
            session.close()
    
    def get_tickets(self):
        """Get all tickets for this attendee"""
        return self.tickets
    
    def has_ticket_for_event(self, event_id):
        """Check if attendee has a ticket for specific event"""
        return any(ticket.event_id == event_id for ticket in self.tickets)