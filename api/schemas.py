from pydantic import BaseModel
from typing import Dict, List, Optional, Any

class Station(BaseModel):
    id: str
    name: str
    lat: float
    lon: float
    city: str

class ForecastResponse(BaseModel):
    station_id: str
    horizon_hours: int
    forecast_value: float
    baseline_value: float
    timestamp: str

class AttributionResponse(BaseModel):
    station_id: str
    modulating_factors: Dict[str, float]
    likely_source_profile: Dict[str, float]

class RecommendationResponse(BaseModel):
    station_id: str
    action: Optional[str]
    advisories: Dict[str, Dict[str, str]]
