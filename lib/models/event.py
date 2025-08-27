from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from . import Base, get_session
from datetime import datetime
from sqlalchemy.orm import relationship, joinedload

class Event(Base):
    # Setting table name to events
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    capacity = Column(Integer, nullable=False)

    #Relationship to tickets
    tickets = relationship("Ticket", back_populates="event", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Event(id={self.id}, name='{self.name}', location='{self.location}', date='{self.date}', capacity={self.capacity})>"
    
    # Property methods 
    @property
    def name_property(self):
        return self._name
    
    # Ensuring name is not empty and doesn’t exceed 100 characters.
    @name_property.setter
    def name_property(self, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Event name cannot be empty")
        if len(value) > 100:
            raise ValueError("Event name cannot exceed 100 characters")
        self._name = value.strip()

    # Ensuring capacity is a positive integer and doesn’t exceed 10,000.
    @property
    def capacity_property(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Capacity must be a positive integer")
        if value > 10000:
            raise ValueError("Capacity cannot exceed 10,000")
        self._capacity = value

    # ORM 
    #  Creating a new Event record in the database
    @classmethod
    def create(cls, name, location, date, capacity):
        """Create a new event"""
        session = get_session()
        try:
            # Validate date
            if isinstance(date, str):
                date = datetime.strptime(date, '%Y-%m-%d').date()
            
            event = cls(name=name, location=location, date=date, capacity=capacity)
            session.add(event)
            session.commit()
            session.refresh(event)
            return event
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    #  Returns all events from the database
    @classmethod
    def get_all(cls):
        """Get all events"""
        session = get_session()
        try:
            from sqlalchemy.orm import joinedload
            return session.query(cls).options(joinedload(cls.tickets)).all()
        finally:
            session.close()
    
    # Returns a single event by its ID
    @classmethod
    def find_by_id(cls, event_id):
        """Find event by ID"""
        session = get_session()
        try:
            return session.query(cls).filter(cls.id == event_id).first()
        finally:
            session.close()
   
    # Deletes this event from the database
    def delete(self):
        """Delete this event"""
        session = get_session()
        try:
            session.delete(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

        # Returns all attendees for this event
    def get_attendees(self):
        """Get all attendees for this event"""
        session = get_session()
        try:
            from .attendee import Attendee
            return session.query(Attendee).join(Attendee.tickets).filter_by(event_id=self.id).all()
        finally:
            session.close()
    # Checks if there are available spots for this event
    def available_spots(self):
        """Get number of available spots"""
        return self.capacity - len(self.tickets)
    
    # Checks if the event is at full capacity
    def is_full(self):
        """Check if event is at capacity"""
        return len(self.tickets) >= self.capacity