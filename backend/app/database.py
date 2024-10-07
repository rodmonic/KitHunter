from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL
DATABASE_URL = "sqlite:///./kit_hunter.db"

# Create the database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # echo=True logs all the SQL queries for debugging

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
