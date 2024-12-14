import radios
from location import geodetic_to_slant_range
from math import pi
import numpy as np

class FreeSpace:
    def path_loss(self,
        transmitter: radios.Transmitter,
        detector_grid: radios.Detector_Grid
     ) -> np.ndarray:
        
        # Convert from Lat Lons to Distance
        slant_ranges_m = geodetic_to_slant_range(transmitter.Lat,transmitter.Lon,0,detector_grid.Lat)
        
        
        # Determine Path Loss
        return np.multiply(np.exp(slant_ranges_m, 2),4*pi)