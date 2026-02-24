from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import settings
from db.models import Base

# Create SQLAlchemy engine
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DB dependency for FastAPI endpoints


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
