import pytest
from datetime import datetime
from services.alert_service import AlertService
from models.weather_data import WeatherData

@pytest.fixture
def mock_settings():
    class MockSettings:
        def get_cities(self):
            return ['TestCity']
    return MockSettings()

@pytest.fixture
def alert_service(mock_settings):
    return AlertService(mock_settings)

def test_set_threshold(alert_service):
    alert_service.set_threshold(30, "TestCity")
    assert alert_service.thresholds["TestCity"] == 30

def test_check_alert(alert_service):
    alert_service.set_threshold(30, "TestCity")
    weather_data = WeatherData(city="TestCity", main="Clear", temp=32, feels_like=34, dt=datetime.fromtimestamp(1622555555))
    alert_service.check_alert(weather_data)
    assert len(alert_service.alerts["TestCity"]) == 1

def test_get_daily_summary(alert_service):
    weather_data = [
        WeatherData(city="TestCity", main="Clear", temp=20, feels_like=22, dt=datetime.fromtimestamp(1622555555)),
        WeatherData(city="TestCity", main="Cloudy", temp=25, feels_like=26, dt=datetime.fromtimestamp(1622565555))
    ]
    summary = alert_service.get_daily_summary("TestCity", weather_data)
    assert summary["avg_temp"] == 22.5
    assert summary["max_temp"] == 25
    assert summary["min_temp"] == 20
