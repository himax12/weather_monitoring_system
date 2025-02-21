from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the database URL from the environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Set up Base, engine, and session
Base = declarative_base()
engine = create_engine(DATABASE_URL)

# Define session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define WeatherDataDB table schema
class WeatherDataDB(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    main = Column(String)
    temp = Column(Float)
    feels_like = Column(Float)
    dt = DateTime

# Create all tables (if they don't exist already)
Base.metadata.create_all(bind=engine)

# Insert weather data into the database
def insert_weather_data(weather_data: dict):
    db_weather_data = WeatherDataDB(**weather_data)
    db = SessionLocal()
    try:
        db.add(db_weather_data)
        db.commit()
        db.refresh(db_weather_data)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Retrieve daily weather data from the database
def get_daily_weather_data(city: str):
    db = SessionLocal()
    try:
        result = db.query(WeatherDataDB).filter(WeatherDataDB.city == city).all()
        return result
    finally:
        db.close()
