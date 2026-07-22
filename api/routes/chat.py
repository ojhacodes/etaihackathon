from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import requests
from typing import Optional

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    station_id: str
    station_name: str
    forecast_data: Optional[list] = None
    attribution_data: Optional[dict] = None
    recommendations: Optional[list] = None

@router.post("/chat/{station_id}")
async def chat_with_advisor(station_id: str, request: ChatRequest):
    # Using GROQ_API_KEY as requested
    api_key = os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        return {"response": "GROQ_API_KEY environment variable is not set. Please configure it in your Render settings."}
    
    global_context = """
Global City Overview (Current Average AQI):
- Delhi: 342 (Severe) - Primary issue: Vehicle Exhaust & Crop Burning
- Mumbai: 156 (Moderate) - Primary issue: Construction Dust
- Bengaluru: 89 (Satisfactory) - Primary issue: Traffic Congestion
- Chennai: 112 (Moderate) - Primary issue: Industrial Emissions
- Kolkata: 210 (Poor) - Primary issue: Road Dust & Vehicles
- Hyderabad: 145 (Moderate) - Primary issue: Construction
- Pune: 178 (Moderate) - Primary issue: Two-wheeler exhaust
- Ahmedabad: 280 (Poor) - Primary issue: Industrial & Dust
- Jaipur: 245 (Poor) - Primary issue: Desert Dust & Vehicles
- Lucknow: 310 (Very Poor) - Primary issue: Biomass Burning & Vehicles
"""

    system_prompt = f"""You are the 'AQI Sentinel AI Advisor', a highly intelligent city planning and pollution mitigation expert.
You have oversight over the entire national network of cities, but the user is currently looking at data for the station: {request.station_name} (ID: {station_id}).

{global_context}

Current Grid Context ({request.station_name}):
- Forecast Trend: {request.forecast_data if request.forecast_data else 'Not provided'}
- Pollution Sources: {request.attribution_data if request.attribution_data else 'Not provided'}
- System Recommendations: {request.recommendations if request.recommendations else 'Not provided'}

If the user asks about this specific grid, use the Current Grid Context.
If the user asks to compare cities or asks which city needs the most focus globally, use the Global City Overview.
Answer concisely and professionally, giving highly specific, actionable advice. Keep responses under 3 paragraphs."""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "openai/gpt-oss-120b", # Using GPT OSS 120B as requested
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.message}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        if response.status_code != 200:
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", response.text)
            return {"response": f"Groq API Error: {error_msg}"}
            
        data = response.json()
        return {"response": data["choices"][0]["message"]["content"]}
    except Exception as e:
        print(f"LLM Error: {e}")
        return {"response": f"An error occurred while contacting the AI API: {str(e)}"}
