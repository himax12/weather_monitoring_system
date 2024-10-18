from pydantic_settings import BaseSettings
from typing import Union, List, Dict

class Settings(BaseSettings):
    OPENWEATHERMAP_API_KEY: str
    DATABASE_URL: str
    CITIES: Union[List[str], Dict[str, Dict[str, float]]] = [
        "Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"
    ]

    class Config:
        env_file = ".env"

    def get_cities(self) -> List[str]:
        if isinstance(self.CITIES, list):
            return self.CITIES
        elif isinstance(self.CITIES, dict):
            return list(self.CITIES.keys())
        else:
            raise ValueError("CITIES must be a list of strings or a dictionary")

    def get_city_coords(self, city: str) -> Dict[str, float]:
        if isinstance(self.CITIES, dict):
            return self.CITIES.get(city, {})
        else:
            return {}
        
        