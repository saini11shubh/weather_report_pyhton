import requests
from datetime import datetime
from sqlalchemy.orm import Session
from .models import WeatherData
from .database import get_db


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_weather(lat: float, lon: float):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m",
        "forecast_days": 3
    }
    response = requests.get(OPEN_METEO_URL, params=params)
    response.raise_for_status()
    return response.json()

def save_to_db(db: Session, data: dict, lat: float, lon: float):
    hourly = data["hourly"]
    timestamps = hourly["time"]
    temps = hourly["temperature_2m"]
    hums = hourly["relative_humidity_2m"]

    for t, temp, hum in zip(timestamps, temps, hums):
        db_obj = WeatherData(
            timestamp=datetime.fromisoformat(t),
            temperature=temp,
            humidity=hum,
            latitude=lat,
            longitude=lon
        )
        db.add(db_obj)
    db.commit()
