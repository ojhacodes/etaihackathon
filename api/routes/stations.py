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
    {"id": "s10", "name": "Jayanagar, Bengaluru", "lat": 12.9299, "lon": 77.5826, "city": "Bengaluru"},
    
    # Chennai
    {"id": "s11", "name": "Adyar, Chennai", "lat": 13.0012, "lon": 80.2565, "city": "Chennai"},
    {"id": "s12", "name": "T Nagar, Chennai", "lat": 13.0418, "lon": 80.2341, "city": "Chennai"},
    {"id": "s13", "name": "Velachery, Chennai", "lat": 12.9759, "lon": 80.2212, "city": "Chennai"},
    
    # Kolkata
    {"id": "s14", "name": "Salt Lake, Kolkata", "lat": 22.5867, "lon": 88.4136, "city": "Kolkata"},
    {"id": "s15", "name": "Ballygunge, Kolkata", "lat": 22.5280, "lon": 88.3659, "city": "Kolkata"},
    {"id": "s16", "name": "Jadavpur, Kolkata", "lat": 22.4955, "lon": 88.3709, "city": "Kolkata"},
    
    # Hyderabad
    {"id": "s17", "name": "Banjara Hills, Hyderabad", "lat": 17.4156, "lon": 78.4347, "city": "Hyderabad"},
    {"id": "s18", "name": "HITEC City, Hyderabad", "lat": 17.4435, "lon": 78.3772, "city": "Hyderabad"},
    {"id": "s19", "name": "Secunderabad, Hyderabad", "lat": 17.4399, "lon": 78.4983, "city": "Hyderabad"}
]

@router.get("/stations", response_model=List[Station])
def get_stations():
    return STATIONS
