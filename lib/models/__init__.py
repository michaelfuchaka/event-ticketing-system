from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up one level to lib/ director
lib_dir = os.path.dirname(current_dir)


# Set database path in the lib directory
db_path = os.path.join(lib_dir, "event_ticketing.db")
DATABASE_URL = f"sqlite:///{db_path}"


# Create Engine
engine =  create_engine(DATABASE_URL)

# Create base class for models
Base = declarative_base()

# Create session factory
SessionLocal  = sessionmaker(autocommit = False, autoflush =  False, bind = engine)

# Function to get database session
def get_session():
    return SessionLocal()

# Function to create all tables
def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)