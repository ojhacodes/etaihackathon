from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import forecast, attribution, recommendation, stations, chat

app = FastAPI(title="AQI Sentinel API", version="2.0")

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stations.router, prefix="/api")
app.include_router(forecast.router, prefix="/api")
app.include_router(attribution.router, prefix="/api")
app.include_router(recommendation.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "AQI Sentinel API v2.0 is running"}
