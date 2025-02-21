import aiohttp
from models.weather_data import WeatherData
from datetime import datetime

class WeatherService:
    def __init__(self, settings):
        self.settings = settings
        self.api_key = settings.OPENWEATHERMAP_API_KEY
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    async def get_current_weather(self, city: str) -> WeatherData:
        # Determine query parameters based on whether coordinates are available
        coords = self.settings.get_city_coords(city)
        if coords:
            params = {
                "lat": coords["lat"],
                "lon": coords["lon"],
                "appid": self.api_key,
                "units": "metric"
            }
        else:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"
            }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Pass dt as an integer timestamp instead of converting it to datetime
                        return WeatherData(
                            city=city,
                            temp=data['main']['temp'],
                            feels_like=data['main']['feels_like'],
                            main=data['weather'][0]['main'],
                            dt=int(data['dt'])
                        )
                    else:
                        error_text = await response.text()
                        raise Exception(f"Failed to fetch weather data for {city}. "
                                        f"Status: {response.status}. Response: {error_text}")
        except Exception as e:
            print(f"Exception occurred in get_current_weather for {city}: {e}")
            raise

    async def fetch_weather_data(self):
        for city in self.settings.get_cities():
            try:
                weather_data = await self.get_current_weather(city)
                # Here you would typically save this data to your database
                # For example: await database_service.save_weather_data(weather_data)
                # And also check for alerts, etc.
                print(f"Fetched weather data for {city}: {weather_data}")
            except Exception as e:
                print(f"Error fetching weather data for {city}: {str(e)}")
