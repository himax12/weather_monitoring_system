import pytest
from datetime import datetime
from utils.weather_analyzer import WeatherAnalyzer
from models.weather_data import WeatherData

@pytest.fixture
def weather_analyzer():
    return WeatherAnalyzer()

def test_get_daily_summary(weather_analyzer, mocker):
    mock_data = [
        WeatherData(city="TestCity", main="Clear", temp=20, feels_like=22, dt=datetime.fromtimestamp(1622555555)),
        WeatherData(city="TestCity", main="Cloudy", temp=25, feels_like=26, dt=datetime.fromtimestamp(1622565555))
    ]
    mocker.patch('data.database.get_daily_weather_data', return_value=mock_data)
    
    summary = weather_analyzer.get_daily_summary("TestCity")
    assert summary["avg_temp"] == 22.5
    assert summary["max_temp"] == 25
    assert summary["min_temp"] == 20
    assert summary["dominant_condition"] == "Clear"