import requests
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .models import WeatherData
from .database import get_db


OPEN_METEO_URL = "https://api.open-meteo.com/v1/meteoswiss"

def fetch_weather(lat: float, lon: float):
    end = datetime.utcnow()
    start = end - timedelta(days=2)
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m",
        "start": start.strftime("%Y-%m-%dT%H:%M"),
        "end": end.strftime("%Y-%m-%dT%H:%M")
    }
    response = requests.get(OPEN_METEO_URL, params=params)
    response.raise_for_status()
    return response.json()

def save_to_db(db: Session, lat: float, lon: float, data: dict):
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
