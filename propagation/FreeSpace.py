import radios
from location import geodetic_to_slant_range
from math import pi
import numpy as np
import antenna.Isotropic

class FreeSpace:
    def path_loss(self,
        transmitter: radios.Transmitter,
        detector_grid: radios.Detector_Grid,
        Freq: radios.Freq,
        Antenna: radios.Antenna
     ) -> np.ndarray:
        
        # Convert from Lat Lons to Distance
        slant_ranges_m = geodetic_to_slant_range(transmitter.Lat,transmitter.Lon,0,detector_grid.Lat)
        # find angle
        theta = 0 # assuming they're pointed at each other
        
        # Determine Path Loss from Goldsmith
        # Determine LOB gain between TX/RX (pg 29)
        if Antenna == "Isotropic":
            tx_lob = antenna.Isotropic.gain(theta)
            rx_lob = antenna.Isotropic.gain(theta)
        g_l = tx_lob*rx_lob
        wavelength = 3e8/Freq
        #return np.multiply(np.exp(slant_ranges_m, 2),4*pi)
        los_loss = np.divide((np.sqrt(g_l)*wavelength),(4*pi*slant_ranges_m)) #this may fail if slant ranges is a vector
        return np.exp(los_loss,2)