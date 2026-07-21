from fastapi import APIRouter
import os
import requests

router = APIRouter()

@router.get("/weather/{lat}/{lon}")
async def get_weather(lat: float, lon: float):
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    if not api_key:
        return {"error": "Weather API key not configured"}
        
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        return {
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"] * 3.6, # Convert m/s to km/h
            "description": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"]
        }
    except Exception as e:
        print(f"Weather API Error: {e}")
        return {"error": "Failed to fetch live weather data"}
