import aiohttp
import pandas as pd
from models.weather_data import WeatherData
from datetime import datetime

class WeatherService:
    def __init__(self, settings):
        """
        Initializes the WeatherService with the given settings.

        :param settings: An object that provides configuration details including:
                         - OPENWEATHERMAP_API_KEY: Your API key for OpenWeatherMap.
                         - get_city_coords(city): A method to fetch coordinates for a city.
                         - get_cities(): A method to return a list of cities to fetch weather data for.
        """
        self.settings = settings
        self.api_key = settings.OPENWEATHERMAP_API_KEY
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    async def get_current_weather(self, city: str) -> WeatherData:
        """
        Fetches the current weather for a given city using the OpenWeatherMap API.

        If coordinates are available for the city via settings.get_city_coords(),
        the API request will use those; otherwise, it will fall back to querying by city name.

        :param city: Name of the city.
        :return: WeatherData instance containing the fetched weather details.
        :raises Exception: If the API call fails.
        """
        # Determine query parameters based on available coordinates
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
                        return WeatherData(
                            city=city,
                            temp=data['main']['temp'],
                            feels_like=data['main']['feels_like'],
                            main=data['weather'][0]['main'],
                            dt=int(data['dt'])  # Keep timestamp as an integer
                        )
                    else:
                        error_text = await response.text()
                        raise Exception(
                            f"Failed to fetch weather data for {city}. "
                            f"Status: {response.status}. Response: {error_text}"
                        )
        except Exception as e:
            print(f"Exception occurred in get_current_weather for {city}: {e}")
            raise

    async def fetch_weather_data(self):
        """
        Iterates over all cities provided by settings.get_cities() and fetches weather data
        for each one. The fetched data can then be saved to a database or processed further.
        """
        cities = self.settings.get_cities()
        for city in cities:
            try:
                weather_data = await self.get_current_weather(city)
                # TODO: Save weather_data to your database or process it further.
                print(f"Fetched weather data for {city}: {weather_data}")
            except Exception as e:
                print(f"Error fetching weather data for {city}: {str(e)}")

    def get_city_weather_data(self, city: str) -> pd.DataFrame:
        """
        Returns a Pandas DataFrame with weather data for the specified city.
        This is a dummy implementation for testing purposes. In production, replace this method
        with your actual data retrieval logic (e.g., querying your database).

        :param city: The city name.
        :return: A Pandas DataFrame containing columns 'timestamp', 'city', 'temperature', and 'humidity'.
        """
        # Dummy data for demonstration
        data = {
            "timestamp": ["2025-02-20 10:00", "2025-02-20 11:00", "2025-02-20 12:00"],
            "city": [city, city, city],
            "temperature": [25, 26, 27],
            "humidity": [30, 35, 40],
        }
        df = pd.DataFrame(data)
        # Ensure the timestamp column is in datetime format
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df
