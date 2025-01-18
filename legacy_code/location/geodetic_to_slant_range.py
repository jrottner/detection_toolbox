from  pyproj import Geod
from typing import Union
import numpy as np

def geodetic_to_slant_rangeClass(
    tx_lat: float, 
    tx_lon: float, 
    tx_alt: float,
    rx_lats: Union[float, np.ndarray], 
    rx_lons: Union[float, np.ndarray], 
    rx_alts: Union[float, np.ndarray]
) -> Union[float,np.ndarray]:
    
    # Initialize geodesic calculator with WGS84 ellipsoid
    geod = Geod(ellps='WGS84')
    
    # Slant range calculation for each receiver poin
    
    # Return as scalar if input was a single point
    if type(rx_lats) is list:
        slant_ranges_m = np.zeros_like(rx_lats, dtype=float)
        for i, (lat, lon, alt) in enumerate(zip(rx_lats, rx_lons, rx_alts)):
            # Calculate geodesic distance (surface distance)
            distance = geod.line_length([tx_lon,lon], [tx_lat,lat])
            
            # Calculate 3D slant range (Pythagorean theorem in 3D)
            altitude_diff = alt - tx_alt
            slant_range = np.sqrt(distance**2 + altitude_diff**2)
            
            slant_ranges_m[i] = slant_range
    else:
        distance = geod.line_length([tx_lon,rx_lons], [tx_lat,rx_lats]) # these are all ints            
        # Calculate 3D slant range (Pythagorean theorem in 3D)
        altitude_diff = rx_alts - tx_alt
        slant_range = np.sqrt(distance**2 + altitude_diff**2)
        # hopefully this doesn't throw another error
        slant_ranges_m = slant_range 

    return slant_ranges_m
    

        