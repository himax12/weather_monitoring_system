import pytest
from fastapi.testclient import TestClient
from main import app, get_weather_api, get_alert_service
from datetime import datetime

client = TestClient(app)

@pytest.fixture
def mock_weather_api(mocker):
    mock_api = mocker.Mock()
    mock_api.get_current_weather.return_value = {
        "city": "TestCity",
        "temperature": 25,
        "feels_like": 26,
        "humidity": 60,
        "description": "Sunny"
    }
    mocker.patch('main.get_weather_api', return_value=mock_api)
    return mock_api

@pytest.fixture
def mock_alert_service(mocker):
    mock_service = mocker.Mock()
    mock_service.get_alerts.return_value = ["Alert 1", "Alert 2"]
    mock_service.get_daily_summary.return_value = {
        "avg_temp": 22.5,
        "max_temp": 25,
        "min_temp": 20,
        "dominant_condition": "Sunny"
    }
    mocker.patch('main.get_alert_service', return_value=mock_service)
    return mock_service

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Weather Monitoring System API"}

def test_get_current_weather(mock_weather_api):
    response = client.get("/current-weather/TestCity")
    assert response.status_code == 200
    assert response.json() == {
        "city": "TestCity",
        "temperature": 25,
        "feels_like": 26,
        "humidity": 60,
        "description": "Sunny"
    }

def test_get_daily_summary(mock_alert_service):
    response = client.get("/daily-summary/TestCity")
    assert response.status_code == 200
    assert response.json() == {
        "avg_temp": 22.5,
        "max_temp": 25,
        "min_temp": 20,
        "dominant_condition": "Sunny"
    }

def test_set_alert_threshold(mock_alert_service):
    response = client.post("/set-alert-threshold", json={"threshold": 30, "city": "TestCity"})
    assert response.status_code == 200
    assert response.json() == {"message": "Alert threshold set to 30°C for TestCity"}
    mock_alert_service.set_threshold.assert_called_once_with(30, "TestCity")

def test_get_alerts(mock_alert_service):
    response = client.get("/alerts/TestCity")
    assert response.status_code == 200
    assert response.json() == ["Alert 1", "Alert 2"]