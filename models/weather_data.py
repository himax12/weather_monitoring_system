from pydantic import BaseModel
from datetime import datetime

class WeatherData(BaseModel):
    city: str
    main: str
    temp: float
    feels_like: float
    dt: int

    @property
    def datetime(self):
        return datetime.fromtimestamp(self.dt)