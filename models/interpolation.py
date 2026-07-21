import numpy as np
from scipy.interpolate import griddata

def interpolate_to_grid(stations, station_values, lat_range, lon_range, resolution=100):
    """
    Interpolate station values to a regular grid using inverse-distance weighting (linear interpolation).
    stations: list of tuples (lat, lon)
    station_values: list of values corresponding to stations
    """
    station_coords = np.array(stations)
    values = np.array(station_values)
    
    # Create grid
    grid_lat, grid_lon = np.mgrid[
        lat_range[0]:lat_range[1]:complex(0, resolution), 
        lon_range[0]:lon_range[1]:complex(0, resolution)
    ]
    
    # Interpolate
    grid_surface = griddata(
        station_coords, values, (grid_lat, grid_lon), method="linear"
    )
    
    return grid_lat, grid_lon, grid_surface

# Mock test
if __name__ == "__main__":
    stations = [(28.6, 77.2), (28.61, 77.25), (28.55, 77.22)]
    values = [250, 310, 180]
    lat_range = (28.5, 28.7)
    lon_range = (77.1, 77.3)
    
    lat, lon, surface = interpolate_to_grid(stations, values, lat_range, lon_range, resolution=50)
    print("Interpolation surface shape:", surface.shape)
