def lat_lon_to_geohash(lat, lon, precision=6):
    """
    Mock geohash implementation.
    In a real system, you would use python-geohash or h3.
    """
    return f"geo_{round(lat, 2)}_{round(lon, 2)}"

def get_neighbors(geohash):
    """
    Mock neighbor lookup for geohash.
    """
    return []
