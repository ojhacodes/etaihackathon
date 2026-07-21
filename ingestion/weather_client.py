import os
import json
import requests
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"

class WeatherClient:
    def __init__(self):
        self.api_key = os.environ.get("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def fetch_current_weather(self, lat, lon):
        """Fetch current weather from OpenWeather API"""
        if not self.api_key:
            return self._mock_weather_data()
            
        try:
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric"
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return self._mock_weather_data()
            
    def _mock_weather_data(self):
        return {
            "main": {
                "temp": 32.5,
                "humidity": 65
            },
            "wind": {
                "speed": 3.5,
                "deg": 120
            }
        }
