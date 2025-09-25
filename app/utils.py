import os
os.environ['MPLBACKEND'] = 'Agg'  # Set backend before any matplotlib imports
import pandas as pd
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
from matplotlib import pyplot as plt
from weasyprint import HTML
from .models import WeatherData

def generate_excel(records, file_stream):
    data = []
    for record in records:
        data.append({
            'timestamp': record.timestamp,
            'temperature': record.temperature,
            'humidity': record.humidity,
            'latitude': record.latitude,
            'longitude': record.longitude
        })
    df = pd.DataFrame(data)
    df.to_excel(file_stream, index=False)

def generate_pdf(records, file_stream):
    data = []
    for record in records:
        data.append({
            'timestamp': record.timestamp,
            'temperature': record.temperature,
            'humidity': record.humidity,
            'latitude': record.latitude,
            'longitude': record.longitude
        })
    
    if not data:
        return
    
    df = pd.DataFrame(data)
    plt.figure(figsize=(10,5))
    plt.plot(df['timestamp'], df['temperature'], label='Temperature (°C)')
    plt.plot(df['timestamp'], df['humidity'], label='Humidity (%)')
    plt.xlabel('Time')
    plt.ylabel('Values')
    plt.title(f'Weather Report: {data[0]["latitude"]}, {data[0]["longitude"]}')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save plot to BytesIO instead of file
    plot_buffer = BytesIO()
    plt.savefig(plot_buffer, format='png', bbox_inches='tight')
    plt.close()
    plot_buffer.seek(0)
    
    # Convert plot to base64 for embedding in HTML
    import base64
    plot_data = base64.b64encode(plot_buffer.getvalue()).decode()
    
    html_content = f"""
    <html>
    <body>
        <h1>Weather Report</h1>
        <p>Location: {data[0]["latitude"]}, {data[0]["longitude"]}</p>
        <img src="data:image/png;base64,{plot_data}" />
    </body>
    </html>
    """
    HTML(string=html_content).write_pdf(file_stream)
