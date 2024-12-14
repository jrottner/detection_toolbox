from  pyproj import Geod
from typing import Union
import numpy as np

def geodetic_to_slant_range(
    tx_lat: float, 
    tx_lon: float, 
    tx_alt: float,
    rx_lats: Union[float, np.ndarray], 
    rx_lons: Union[float, np.ndarray], 
    rx_alts: Union[float, np.ndarray]
) -> Union[float,np.ndarray]:
    
    # Initialize geodesic calculator with WGS84 ellipsoid
    geod = Geod(ellps='WGS84')
    
    # Slant range calculation for each receiver point
    slant_ranges_m = np.zeros_like(rx_lats, dtype=float)
    
    for i, (lat, lon, alt) in enumerate(zip(rx_lats, rx_lons, rx_alts)):
        # Calculate geodesic distance (surface distance)
        distance = geod.line_length([tx_lon,lon], [tx_lat,lat])
        
        # Calculate 3D slant range (Pythagorean theorem in 3D)
        altitude_diff = alt - tx_alt
        slant_range = np.sqrt(distance**2 + altitude_diff**2)
        
        slant_ranges_m[i] = slant_range
    
    # Return as scalar if input was a single point
    return slant_ranges_m[0] if len(slant_ranges_m) == 1 else slant_ranges_m
        