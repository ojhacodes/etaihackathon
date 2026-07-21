from fastapi import APIRouter
from datetime import datetime
import random
from ..schemas import ForecastResponse

router = APIRouter()

@router.get("/forecast/{station_id}", response_model=ForecastResponse)
def get_forecast(station_id: str, horizon: int = 24):
    """Get the forecast for a specific station."""
    # Mock response
    current_val = random.uniform(100, 350)
    forecast_val = current_val * random.uniform(0.8, 1.2)
    
    return {
        "station_id": station_id,
        "horizon_hours": horizon,
        "forecast_value": round(forecast_val, 2),
        "baseline_value": round(current_val, 2),
        "timestamp": datetime.now().isoformat()
    }
