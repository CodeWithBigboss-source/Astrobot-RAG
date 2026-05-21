from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "astrobot_db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Planet(Base):
    __tablename__ = "planets"
    id             = Column(Integer, primary_key=True, index=True)
    name           = Column(String(100), unique=True, nullable=False)
    type           = Column(String(100))
    mass           = Column(Float)
    radius         = Column(Float)
    distance_from_sun = Column(Float)
    orbital_period = Column(Float)
    moons          = Column(Integer)
    description    = Column(Text)
    created_at     = Column(DateTime, default=datetime.utcnow)

class NasaMission(Base):
    __tablename__ = "nasa_missions"
    id             = Column(Integer, primary_key=True, index=True)
    name           = Column(String(200), nullable=False)
    launch_date    = Column(String(50))
    status         = Column(String(100))
    target         = Column(String(200))
    description    = Column(Text)
    agency         = Column(String(100))
    created_at     = Column(DateTime, default=datetime.utcnow)

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id         = Column(Integer, primary_key=True, index=True)
    question   = Column(Text, nullable=False)
    answer     = Column(Text, nullable=False)
    sources    = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")