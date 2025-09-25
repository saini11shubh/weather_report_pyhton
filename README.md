# Weather Report API

A FastAPI-based weather reporting service that fetches weather data from Open-Meteo API and provides data export functionality in PDF and Excel formats.

## Features

- 🌤️ Fetch weather data for any global location
- 📊 Export weather data as Excel files
- 📄 Generate PDF reports with weather charts
- 🗄️ SQLite database storage
- 🚀 FastAPI with automatic API documentation

## Installation & Setup

### Using Python (Recommended)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Access the API:**
   - API Base URL: `http://127.0.0.1:8000`
   - Interactive Documentation: `http://127.0.0.1:8000/docs`

### Using Docker

```bash
docker-compose up --build
```

## API Endpoints

### 1. Weather Report (Fetch & Store Data)

Fetches weather data from Open-Meteo API and stores it in the database.

**Endpoint:** `GET /weather-report`

**Parameters:**
- `lat` (float, required): Latitude coordinate
- `lon` (float, required): Longitude coordinate

**cURL Example:**
```bash
curl -X 'GET' 'http://127.0.0.1:8000/weather-report?lat=28.6139&lon=77.2090' \
  -H 'accept: application/json'
```

**Response:**
```json
{
  "message": "Weather data fetched and saved successfully."
}
```

**Browser URL:**
```
http://127.0.0.1:8000/weather-report?lat=28.6139&lon=77.2090
```

### 2. Export Excel

Downloads weather data as an Excel file (.xlsx).

**Endpoint:** `GET /export/excel`

**cURL Example:**
```bash
curl -X 'GET' 'http://127.0.0.1:8000/export/excel' \
  -H 'accept: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' \
  --output weather_data.xlsx
```

**Browser URL:**
```
http://127.0.0.1:8000/export/excel
```

**Response:** Downloads `weather_data.xlsx` file containing:
- Timestamp
- Temperature (°C)
- Humidity (%)
- Latitude
- Longitude

### 3. Export PDF

Generates a PDF report with weather charts and data.

**Endpoint:** `GET /export/pdf`

**cURL Example:**
```bash
curl -X 'GET' 'http://127.0.0.1:8000/export/pdf' \
  -H 'accept: application/pdf' \
  --output weather_report.pdf
```

**Browser URL:**
```
http://127.0.0.1:8000/export/pdf
```

**Response:** Downloads `weather_report.pdf` file containing:
- Weather report title
- Location coordinates
- Temperature and humidity trend chart

## Complete Workflow Example

1. **Fetch weather data for Delhi:**
   ```bash
   curl -X 'GET' 'http://127.0.0.1:8000/weather-report?lat=28.6139&lon=77.2090' \
     -H 'accept: application/json'
   ```

2. **Download PDF report:**
   ```bash
   curl -X 'GET' 'http://127.0.0.1:8000/export/pdf' \
     -H 'accept: application/pdf' \
     --output weather_report.pdf
   ```

3. **Download Excel data:**
   ```bash
   curl -X 'GET' 'http://127.0.0.1:8000/export/excel' \
     -H 'accept: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' \
     --output weather_data.xlsx
   ```

## API Documentation

Visit `http://127.0.0.1:8000/docs` for interactive API documentation with:
- Try-it-out functionality
- Request/response examples
- Schema definitions
- Parameter descriptions

## Data Sources

- **Weather Data:** [Open-Meteo API](https://open-meteo.com/)
- **Database:** SQLite (local file: `weather.db`)
- **Charts:** Matplotlib
- **PDF Generation:** WeasyPrint

## Error Handling

- **404 Not Found:** No weather data available for export
- **500 Internal Server Error:** API or data processing issues
- **422 Unprocessable Entity:** Invalid parameter values

## Requirements

- Python 3.8+
- FastAPI
- SQLAlchemy
- Matplotlib
- WeasyPrint
- Pandas
- OpenPyXL
- Requests

## Notes

- Weather data is fetched for the next 3 days (forecast)
- Database stores up to 48 recent weather records
- PDF reports include embedded charts as base64 images
- All coordinates use decimal degrees format
