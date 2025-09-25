# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from .database import Base, engine, get_db
from .services import fetch_weather, save_to_db
from .models import WeatherData
from .utils import generate_excel, generate_pdf

import io

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Weather Report API")

# Endpoint: Fetch & store weather data
@app.get("/weather-report")
def weather_report(lat: float, lon: float, db: Session = Depends(get_db)):
    try:
        data = fetch_weather(lat, lon)
        save_to_db(db, data, lat, lon)
        return {"message": "Weather data fetched and saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint: Export Excel
@app.get("/export/excel")
def export_excel(db: Session = Depends(get_db)):
    records = db.query(WeatherData).order_by(WeatherData.timestamp.desc()).limit(48).all()
    if not records:
        raise HTTPException(status_code=404, detail="No weather data found.")
    
    file_stream = io.BytesIO()
    generate_excel(records, file_stream)
    file_stream.seek(0)
    return StreamingResponse(file_stream, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=weather_data.xlsx"})

# Endpoint: Export PDF
@app.get("/export/pdf")
def export_pdf(db: Session = Depends(get_db)):
    records = db.query(WeatherData).order_by(WeatherData.timestamp.desc()).limit(48).all()
    if not records:
        raise HTTPException(status_code=404, detail="No weather data found.")
    
    file_stream = io.BytesIO()
    generate_pdf(records, file_stream)
    file_stream.seek(0)
    return StreamingResponse(file_stream, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=weather_report.pdf"})
