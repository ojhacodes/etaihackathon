import os
import json
import requests
from datetime import datetime
from pathlib import Path

# Setup paths
DATA_DIR = Path(__file__).parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"

class CPCBClient:
    def __init__(self):
        self.api_key = os.environ.get("CPCB_API_KEY")
        self.base_url = "https://api.data.gov.in/resource/3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69"

    def fetch_live_data(self):
        """Fetch live station data from CPCB data.gov.in endpoint"""
        if not self.api_key:
            print("Warning: CPCB_API_KEY not found. Using mock data.")
            return self._mock_live_data()
        
        try:
            params = {
                "api-key": self.api_key,
                "format": "json",
                "limit": 1000
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Save raw data
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = RAW_DIR / f"cpcb_live_{timestamp}.json"
            with open(file_path, "w") as f:
                json.dump(data, f)
            return data
            
        except Exception as e:
            print(f"Error fetching live data: {e}")
            return self._mock_live_data()
            
    def _mock_live_data(self):
        # Provide some mock data for Delhi stations
        return {
            "records": [
                {"station": "Anand Vihar, Delhi - DPCC", "city": "Delhi", "state": "Delhi", "pollutant_id": "PM2.5", "pollutant_min": 100, "pollutant_max": 300, "pollutant_avg": 250},
                {"station": "ITO, Delhi - CPCB", "city": "Delhi", "state": "Delhi", "pollutant_id": "PM2.5", "pollutant_min": 150, "pollutant_max": 400, "pollutant_avg": 310},
                {"station": "Punjabi Bagh, Delhi - DPCC", "city": "Delhi", "state": "Delhi", "pollutant_id": "PM2.5", "pollutant_min": 80, "pollutant_max": 200, "pollutant_avg": 180},
                {"station": "Okhla Phase-2, Delhi - DPCC", "city": "Delhi", "state": "Delhi", "pollutant_id": "PM2.5", "pollutant_min": 120, "pollutant_max": 350, "pollutant_avg": 290}
            ]
        }

if __name__ == "__main__":
    client = CPCBClient()
    client.fetch_live_data()
