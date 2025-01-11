import numpy as np
from pyproj import Geod

def calc_gain(theta):
    return 1

def path_loss(fc,tx_pos, tx_antenna, rx_pos, rx_antenna):

    geod = Geod(ellps='WGS84')
    distance = geod.line_length([tx_pos[0],rx_pos[0]], [tx_pos[1],rx_pos[1]])
    theta = 0

    if tx_antenna == "Isotropic":
        tx_lob = calc_gain(theta)
    else:
        tx_lob = 1
    if rx_antenna == "Isotropic":
        rx_lob = calc_gain(theta)
    else:
        rx_lob = 1
    
    g_l = tx_lob*rx_lob
    wavelength = 3e8/fc
    #return np.multiply(np.exp(slant_ranges_m, 2),4*pi)
    los_loss = np.divide((np.sqrt(g_l)*wavelength),(4*np.pi*distance)) #this may fail if slant ranges is a vector
    return np.log10(np.square(los_loss))

def calc_snr(fc,mod):
    if mod == "SINCGARS":
        bw = 5e3 # nbfm
        R = 16e3 # data rate of sincgars; 16 kbps
    rx_snr = 2**(R/bw) - 1
    return 10*np.log10(rx_snr)

def detector_grid(tx_pos, rx_pos):
    # detector_grid: returns a 3-by-100 ndarray of latlon + alt coordinates
    # tx_pos = [lat,lon,tx_alt]: tx position
    # rx_pos = [lat,lon,rx_alt]: rx position
    # first, find distance between two positions
    geod = Geod(ellps='WGS84')
    #geod = Geod(ellps='clrk66')
    distance = geod.line_length([tx_pos[0],rx_pos[0]], [tx_pos[1],rx_pos[1]])
    altitude_diff = rx_pos[2] - tx_pos[2]
    # logarthmic scale factor from 0 to 100 (10**2) * distance
    npoints = 100
    dg_pos = np.ones((len(tx_pos),npoints))
    aztx_rx, _, distance = geod.inv(tx_pos[0],tx_pos[1], rx_pos[0],rx_pos[1])
    dg_az = np.abs(altitude_diff) * np.logspace(0.01,2,npoints)
    dg_distances = distance * np.logspace(0.01,2,npoints)
    for i in range(npoints):
        dg_pos[0,i], dg_pos[1,i], _ = geod.fwd(tx_pos[0], 
            tx_pos[1], aztx_rx, dg_distances[i])
        dg_pos[2,i] = dg_az[i]

    return dg_pos