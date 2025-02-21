from pydantic import BaseModel, Field
from datetime import datetime

class WeatherData(BaseModel):
    city: str
    main: str
    temp: float
    feels_like: float
    dt: int = Field(default_factory=lambda: int(datetime.now().timestamp()))  # Ensures dt gets a timestamp

    @property
    def datetime(self) -> datetime:
        return datetime.fromtimestamp(self.dt)  # Convert timestamp to datetime

