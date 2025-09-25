import pandas as pd
from io import BytesIO
from matplotlib import pyplot as plt
from weasyprint import HTML
from .models import WeatherData

def generate_excel(data):
    df = pd.DataFrame(data)
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output

def generate_pdf(data, lat, lon):
    df = pd.DataFrame(data)
    plt.figure(figsize=(10,5))
    plt.plot(df['timestamp'], df['temperature'], label='Temperature (°C)')
    plt.plot(df['timestamp'], df['humidity'], label='Humidity (%)')
    plt.xlabel('Time')
    plt.ylabel('Values')
    plt.title(f'Weather Report: {lat}, {lon}')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("chart.png")
    plt.close()

    html_content = f"""
    <h1>Weather Report</h1>
    <p>Location: {lat}, {lon}</p>
    <img src="chart.png" />
    """
    pdf = BytesIO()
    HTML(string=html_content).write_pdf(pdf)
    pdf.seek(0)
    return pdf
