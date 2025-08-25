from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration
DATABASE_URL = "sqlite:///event_ticketing.db"

# Create Engine
engine =  create_engine(DATABASE_URL, echo=True)

# Create base class for models
Base = declarative_base()

# Create session factory
SessionLocal  = sessionmaker(automatic = False, autoflush =  False, bind = engine)

# Function to get database session
def get_session():
    return SessionLocal()