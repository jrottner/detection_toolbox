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
        bw = 12.5e3 # sincgars assumptiona
        R = 16e3 # data rate of sincgars; 16 kbps
        # are these ok assumptions? channel capacity, not link capacity.
    rx_snr = 2**(R/bw) - 1
    # even though this is db, be careful about comparison
    # 3 db fudge factor
    return 10*np.log10(rx_snr) + 3

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
    dg_az = np.abs(altitude_diff) * np.logspace(-1, 1,npoints)
    dg_distances = distance * np.logspace(-1, 1,npoints)
    for i in range(npoints):
        dg_pos[0,i], dg_pos[1,i], _ = geod.fwd(tx_pos[0], 
            tx_pos[1], aztx_rx, dg_distances[i])
        dg_pos[2,i] = dg_az[i]

    return dg_pos

def heatmap(tx_pos, rx_pos):
    # heatmap: returns a 3-by-100 ndarray of latlon + alt coordinates
    # tx_pos = [lat,lon,tx_alt]: tx position
    # rx_pos = [lat,lon,rx_alt]: rx position
    # first, find distance between two positions
    geod = Geod(ellps='WGS84')
    #geod = Geod(ellps='clrk66')
    distance = geod.line_length([tx_pos[0],rx_pos[0]], [tx_pos[1],rx_pos[1]])
    altitude_diff = rx_pos[2] - tx_pos[2]
    # logarthmic scale factor from 0 to 100 (10**2) * distance
    npoints = 50
    dg_pos = np.ones((len(tx_pos),npoints))
    aztx_rx, _, distance = geod.inv(tx_pos[0],tx_pos[1], rx_pos[0],rx_pos[1])
    if aztx_rx > 90 or aztx_rx < 0:
        x_az = 180
    else:
        x_az = 0
    dg_az = np.abs(altitude_diff) * np.logspace(-1, 1,npoints)

    # hold azimuth at quadrant-based 0 or 180 degrees and find a maximum x range ("rx + x")
    dg_distances = distance * np.logspace(-1, 2,npoints)
    heatmap_pos = np.zeros((npoints,npoints,3)) 
    heatmap_axis = np.zeros((npoints,2))
    heatmap_axis[:,0], heatmap_axis[:,1], _ = geod.fwd(np.tile(tx_pos[0],npoints), np.tile(tx_pos[1],npoints), np.tile(x_az,npoints), dg_distances) 
    heatmap_pos[:,0,:2] = heatmap_axis # vector of lat/lon pairs along "x-axis" (y=0)
    heatmap_axis[:,0], heatmap_axis[:,1], _ = geod.fwd(np.tile(tx_pos[0],npoints), np.tile(tx_pos[1],npoints), np.tile(np.sign(aztx_rx)*(90),npoints), 0.25*dg_distances) # fix this one? 
    heatmap_pos[0,:,:2] = heatmap_axis # vector of lat/lon pairs along "y-axis" (x=0)
    for i in range(1,npoints):
        for j in range(1,npoints):
            # take lat [0] along y [0,:,~] axis (x=0), take lon [1] along x [:,0,~] axis (y=0)
            heatmap_pos[i,j,:2] = np.array([heatmap_pos[0,j,0], heatmap_pos[i,0,1]]) #j,i
    return heatmap_pos

def hata(fc,tx_pos, rx_pos, cell_type):
    geod = Geod(ellps='WGS84')
    d = geod.line_length([tx_pos[0],rx_pos[0]], [tx_pos[1],rx_pos[1]])
    fc = fc/(1e6)
    d = d/(1e3)
    if rx_pos[2] == 0:
        alpha = 0
    else:
        alpha = (1.1*np.log10(fc)-0.7)*rx_pos[2] - (1.56*np.log10(fc)-0.8) #dB
    if fc > 300 and rx_pos[2] > 0:
        alpha = 3.2*np.log10(11.75*rx_pos[2])**2 - 4.97
    if tx_pos[2] == 0:
        h_fac = 0
        h_fac_2 = 0
    else:
        h_fac = -13.82*np.log10(tx_pos[2])
        h_fac_2 = -6.55*np.log10(tx_pos[2])
    urban_loss = 69.55 + 26.16*np.log10(fc)+ h_fac - alpha + (44.9+h_fac_2)*np.log10(d)
    if cell_type == 'urban':
        loss = urban_loss
    elif cell_type == 'suburban':
        loss = urban_loss - 2*(np.log10(fc/28))**2 - 5.4
    elif cell_type == 'rural':
        K = 38
        loss = urban_loss - 4.78*(np.log10(fc))**2 + 18.33*np.log10(fc) - K
    return -loss