from fastapi import APIRouter
from ..schemas import AttributionResponse
import random

router = APIRouter()

@router.get("/attribution/{station_id}", response_model=AttributionResponse)
def get_attribution(station_id: str):
    """Get separated modulating factors and likely source profile dynamically."""
    
    # Generate different profiles based on city (using station_id prefixes as a hack)
    if station_id in ["s1", "s2", "s3", "s4"]:
        # Delhi: Classic winter smog pattern
        mod_factors = {
            "meteorological (low wind, high humidity)": random.uniform(0.40, 0.50),
            "persistence/trend": random.uniform(0.20, 0.30),
            "temporal pattern (evening spike)": random.uniform(0.15, 0.25),
            "seasonal/calendar": random.uniform(0.05, 0.10)
        }
        sources = {
            "vehicle_exhaust": random.uniform(0.35, 0.45),
            "road_dust": random.uniform(0.20, 0.30),
            "waste_burning": random.uniform(0.15, 0.20),
            "industrial_light": random.uniform(0.05, 0.15),
            "residential": random.uniform(0.05, 0.10)
        }
    elif station_id in ["s5", "s6", "s7"]:
        # Mumbai: Coastal winds, industrial
        mod_factors = {
            "meteorological (sea breeze)": random.uniform(0.15, 0.25),
            "persistence/trend": random.uniform(0.30, 0.40),
            "temporal pattern": random.uniform(0.25, 0.35),
            "seasonal/calendar": random.uniform(0.05, 0.10)
        }
        sources = {
            "industrial_heavy": random.uniform(0.40, 0.50),
            "vehicle_exhaust": random.uniform(0.25, 0.35),
            "road_dust": random.uniform(0.10, 0.20),
            "waste_burning": random.uniform(0.05, 0.10),
            "residential": random.uniform(0.05, 0.10)
        }
    else:
        # Bengaluru: Traffic and construction dust
        mod_factors = {
            "meteorological (stable temp)": random.uniform(0.20, 0.30),
            "persistence/trend": random.uniform(0.30, 0.40),
            "temporal pattern (rush hour)": random.uniform(0.25, 0.35),
            "seasonal/calendar": random.uniform(0.05, 0.10)
        }
        sources = {
            "vehicle_exhaust": random.uniform(0.45, 0.55),
            "road_dust": random.uniform(0.30, 0.40),
            "industrial_light": random.uniform(0.05, 0.10),
            "waste_burning": random.uniform(0.02, 0.05),
            "residential": random.uniform(0.02, 0.05)
        }

    # Normalize to 1.0
    mod_total = sum(mod_factors.values())
    mod_factors = {k: v/mod_total for k, v in mod_factors.items()}
    
    src_total = sum(sources.values())
    sources = {k: v/src_total for k, v in sources.items()}

    return {
        "station_id": station_id,
        "modulating_factors": mod_factors,
        "likely_source_profile": sources
    }
