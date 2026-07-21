import json
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"

class APnAInventory:
    def __init__(self):
        self.grid_file = RAW_DIR / "apna_grid.csv"

    def download_and_parse(self):
        """Mock parsing of UrbanEmissions.Info APnA program inventory."""
        print("Simulating APnA inventory download and parsing...")
        
        # We simulate what the parsed grid will look like
        mock_grid = pd.DataFrame({
            "lat": [28.6, 28.61, 28.62, 28.63],
            "lon": [77.2, 77.21, 77.22, 77.23],
            "vehicle_exhaust": [0.4, 0.35, 0.5, 0.2],
            "road_dust": [0.3, 0.4, 0.2, 0.5],
            "waste_burning": [0.1, 0.05, 0.1, 0.1],
            "industrial": [0.1, 0.1, 0.1, 0.1],
            "residential": [0.1, 0.1, 0.1, 0.1]
        })
        
        # Ensure dir exists
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        
        mock_grid.to_csv(self.grid_file, index=False)
        print(f"Saved parsed APnA grid to {self.grid_file}")
        
if __name__ == "__main__":
    inventory = APnAInventory()
    inventory.download_and_parse()
