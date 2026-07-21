from fastapi import APIRouter
from typing import List
from ..schemas import Station

router = APIRouter()

STATIONS = [
    # Delhi
    {"id": "s1", "name": "Anand Vihar, Delhi", "lat": 28.6476, "lon": 77.3158, "city": "Delhi"},
    {"id": "s2", "name": "ITO, Delhi", "lat": 28.6286, "lon": 77.2411, "city": "Delhi"},
    {"id": "s3", "name": "Punjabi Bagh, Delhi", "lat": 28.6740, "lon": 77.1310, "city": "Delhi"},
    {"id": "s4", "name": "Okhla Phase-2, Delhi", "lat": 28.5308, "lon": 77.2713, "city": "Delhi"},
    
    # Mumbai
    {"id": "s5", "name": "Bandra, Mumbai", "lat": 19.0596, "lon": 72.8295, "city": "Mumbai"},
    {"id": "s6", "name": "Worli, Mumbai", "lat": 19.0169, "lon": 72.8166, "city": "Mumbai"},
    {"id": "s7", "name": "Colaba, Mumbai", "lat": 18.9067, "lon": 72.8147, "city": "Mumbai"},
    
    # Bengaluru
    {"id": "s8", "name": "Koramangala, Bengaluru", "lat": 12.9279, "lon": 77.6271, "city": "Bengaluru"},
    {"id": "s9", "name": "Indiranagar, Bengaluru", "lat": 12.9784, "lon": 77.6408, "city": "Bengaluru"},
    {"id": "s10", "name": "Jayanagar, Bengaluru", "lat": 12.9299, "lon": 77.5826, "city": "Bengaluru"}
]

@router.get("/stations", response_model=List[Station])
def get_stations():
    return STATIONS
