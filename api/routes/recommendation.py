from fastapi import APIRouter
from ..schemas import RecommendationResponse

router = APIRouter()

def get_mock_severity(aqi_value):
    if aqi_value <= 50: return "Good"
    if aqi_value <= 100: return "Satisfactory"
    if aqi_value <= 200: return "Moderate"
    if aqi_value <= 300: return "Poor"
    if aqi_value <= 400: return "Very Poor"
    return "Severe"

@router.get("/recommendation/{station_id}", response_model=RecommendationResponse)
def get_recommendation(station_id: str):
    """Get recommendations and advisories dynamically based on station."""
    
    # We map back to the dominant source created in attribution.py
    if station_id in ["s1", "s2", "s3", "s4"]:
        # Delhi (Vehicle Exhaust / Waste Burning dominant)
        mock_aqi = 320
        action = "Suggest temporary heavy-vehicle restriction on identified corridor; issue strict fines for waste burning in zone."
    elif station_id in ["s5", "s6", "s7"]:
        # Mumbai (Industrial dominant)
        mock_aqi = 210
        action = "Suggest immediate compliance check for registered heavy industrial units in the coastal zone."
    else:
        # Bengaluru (Vehicle Exhaust / Road Dust dominant)
        mock_aqi = 180
        action = "Suggest water-sprinkling on flagged construction road segments; flag for increased public transit frequency."

    severity = get_mock_severity(mock_aqi)
    
    advisories = {
        "en": {
            "schools": f"AQI forecast: {severity} ({mock_aqi}). Avoid outdoor assembly.",
            "hospitals": f"AQI forecast: {severity} ({mock_aqi}). Expect possible respiratory cases.",
            "outdoor_workers": f"AQI forecast: {severity} ({mock_aqi}). N95 mask recommended."
        },
        "hi": {
            "schools": f"वायु गुणवत्ता पूर्वानुमान: {severity} ({mock_aqi})। बाहरी सभा से बचें।",
            "hospitals": f"वायु गुणवत्ता पूर्वानुमान: {severity} ({mock_aqi})। श्वसन संबंधी मामलों की संभावना।",
            "outdoor_workers": f"वायु गुणवत्ता पूर्वानुमान: {severity} ({mock_aqi})। N95 मास्क की सलाह।"
        }
    }
    
    return {
        "station_id": station_id,
        "action": action,
        "advisories": advisories
    }
