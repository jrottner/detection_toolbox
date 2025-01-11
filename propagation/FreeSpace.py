import radios
from location import geodetic_to_slant_range
from math import pi
import numpy as np
import antenna.Isotropic

class FreeSpaceClass:
    def path_loss(self,
        transmitter: radios.Transmitter,
        detector_grid: radios.Detector_Grid,
        #Freq: radios.Transmitter.
        #Antenna: radios.Antenna
     ) -> np.ndarray:
        
        # Convert from Lat Lons to Distance
        # fix this function -> detector grid should return lat/lon grid from build_ll_grid function
        [ll_lat, ll_lon] = detector_grid.build_ll_grid() # returns [lat, lon]
        # print(ll_lat,ll_lon)
        slant_ranges_m = geodetic_to_slant_range.geodetic_to_slant_rangeClass(transmitter.Lat,transmitter.Lon,0,ll_lat,ll_lon,0)
        
        # some map from slant_ranges_m to theta
        theta = 0

        if transmitter.Antenna == "Isotropic":
            tx_lob = antenna.Isotropic.Isotropic.gain(theta)
            rx_lob = antenna.Isotropic.Isotropic.gain(theta)
        else:
            tx_lob = 1
            rx_lob = 1
        
        g_l = tx_lob*rx_lob
        wavelength = 3e8/transmitter.Freq
        #return np.multiply(np.exp(slant_ranges_m, 2),4*pi)
        los_loss = np.divide((np.sqrt(g_l)*wavelength),(4*pi*slant_ranges_m)) #this may fail if slant ranges is a vector
        return np.square(los_loss)
