from pydantic import BaseModel
from datetime import datetime

class WeatherDataSchema(BaseModel):
    timestamp: datetime
    temperature: float
    humidity: float
    latitude: float
    longitude: float

    class Config:
        orm_mode = True
