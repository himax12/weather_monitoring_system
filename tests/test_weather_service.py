# Content of test_weather_service.py
import pytest
from unittest.mock import patch, MagicMock
from services.weather_service import WeatherService
from config.settings import Settings

@pytest.fixture
def weather_service():
    settings = Settings(OPENWEATHERMAP_API_KEY="test_key", DATABASE_URL="sqlite:///./test.db")
    return WeatherService(settings)

@patch('httpx.AsyncClient.get')
async def test_fetch_weather_data(mock_get, weather_service):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "weather": [{"main": "Clear"}],
        "main": {"temp": 20, "feels_like": 22},
        "dt": 1622555555
    }
    mock_get.return_value = mock_response

    await weather_service.fetch_weather_data()
    
    mock_get.assert_called_once()
    # Add assertions to check if data was properly processed and stored

async def test_get_current_weather(weather_service):
    with patch.object(weather_service, '_make_api_call') as mock_api_call:
        mock_api_call.return_value = {"temp": 25, "humidity": 60}
        result = await weather_service.get_current_weather("TestCity")
        assert result == {"temp": 25, "humidity": 60}
