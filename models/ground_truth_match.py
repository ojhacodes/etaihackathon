import pandas as pd
from pathlib import Path

# In a real app we'd load the generated grid from ingestion
DATA_DIR = Path(__file__).parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"

def load_apna_inventory(city="delhi_2018emi"):
    """Load APnA inventory. Mocked for now."""
    grid_file = RAW_DIR / "apna_grid.csv"
    if grid_file.exists():
        return pd.read_csv(grid_file)
    
    # Mock data if file doesn't exist
    return pd.DataFrame({
        "lat": [28.6, 28.61, 28.62, 28.63],
        "lon": [77.2, 77.21, 77.22, 77.23],
        "vehicle_exhaust": [0.4, 0.35, 0.5, 0.2],
        "road_dust": [0.3, 0.4, 0.2, 0.5],
        "waste_burning": [0.1, 0.05, 0.1, 0.1],
        "industrial_heavy": [0.05, 0.05, 0.05, 0.05],
        "industrial_light": [0.05, 0.05, 0.05, 0.05],
        "residential": [0.1, 0.1, 0.1, 0.1]
    })

def nearest_grid_cell(lat, lon, grid_df):
    """Find nearest grid cell in APnA inventory."""
    # Simple Euclidean distance for mock
    dist = (grid_df['lat'] - lat)**2 + (grid_df['lon'] - lon)**2
    nearest_idx = dist.idxmin()
    return grid_df.iloc[nearest_idx]

def get_likely_source_profile(station_lat, station_lon):
    """
    Get the likely source profile for a station based on the independent 
    ground-truth APnA inventory.
    """
    grid = load_apna_inventory()
    cell = nearest_grid_cell(station_lat, station_lon, grid)
    
    sectors = ["vehicle_exhaust", "road_dust", "waste_burning", 
               "industrial_heavy", "industrial_light", "residential"]
               
    profile = {}
    for sector in sectors:
        if sector in cell:
            profile[sector] = float(cell[sector])
            
    return profile
