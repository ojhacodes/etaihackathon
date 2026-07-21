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
    # Using OPENROUTER_API_KEY as requested
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    if not api_key:
        return {"response": "OPENROUTER_API_KEY environment variable is not set. Please configure it in your Render settings."}
    
    system_prompt = f"""You are the 'AQI Sentinel AI Advisor', a highly intelligent city planning and pollution mitigation expert.
You are currently looking at data for the station: {request.station_name} (ID: {station_id}).

Current Data Context:
- Forecast Trend: {request.forecast_data if request.forecast_data else 'Not provided'}
- Pollution Sources: {request.attribution_data if request.attribution_data else 'Not provided'}
- System Recommendations: {request.recommendations if request.recommendations else 'Not provided'}

Answer the user's questions concisely and professionally, using the provided data to give highly specific, actionable advice.
Keep responses under 3 paragraphs. Use markdown for readability."""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://etaihackathon.vercel.app/", # Optional, for including your app on openrouter.ai rankings.
        "X-Title": "AQI Sentinel" # Optional. Shows in rankings on openrouter.ai.
    }
    
    payload = {
        "model": "meta-llama/llama-3-70b-instruct", # Using a highly capable OSS model
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": request.message}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        if response.status_code != 200:
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", response.text)
            return {"response": f"OpenRouter API Error: {error_msg}"}
            
        data = response.json()
        return {"response": data["choices"][0]["message"]["content"]}
    except Exception as e:
        print(f"LLM Error: {e}")
        return {"response": f"An error occurred while contacting the AI API: {str(e)}"}
