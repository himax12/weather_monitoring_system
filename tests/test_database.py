# Content of test_database.py
import pytest
from sqlalchemy.orm import Session
from data.database import insert_weather_data, get_daily_weather_data, WeatherDataDB
from models.weather_data import WeatherData

@pytest.fixture
def db_session():
    # Set up a test database session
    # This could be an in-memory SQLite database for testing
    pass

async def test_insert_weather_data(db_session):
    weather_data = WeatherData(city="TestCity", main="Clear", temp=20, feels_like=22, dt=1622555555)
    await insert_weather_data(weather_data)
    
    result = db_session.query(WeatherDataDB).filter_by(city="TestCity").first()
    assert result is not None
    assert result.temp == 20
    assert result[1].temp == 25


def test_get_daily_weather_data(db_session):
    # Insert some test data
    db_session.add(WeatherDataDB(city="TestCity", main="Clear", temp=20, feels_like=22, dt=1622555555))
    db_session.add(WeatherDataDB(city="TestCity", main="Cloudy", temp=25, feels_like=26, dt=1622565555))
    db_session.commit()

    result = get_daily_weather_data("TestCity")
    assert len(result) == 2
    assert result[0].temp == 20