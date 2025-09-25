from sqlalchemy import Column, Integer, Float, String, DateTime
from .database import Base

class WeatherData(Base):
    __tablename__ = "weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
