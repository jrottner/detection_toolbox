import numpy as np
import calculations
# specify simulation information

# first, user information:
fc = 80e6                                       # carrier freq at 80 MHz (Sincgars)
tx_pos = np.array([33.420732,-82.143516,0])     # lat, lon, altitude (m)
mod = "SINCGARS"                                # string for modulation type (determines RX SNR)
tx_antenna = "Isotropic"                        # string for antenna type
tx_pwr = 100                                    # tx power, in watts
tx_pwr_db = 10*np.log10(tx_pwr)                 # tx power, in dB

# specify friendly information:
rx_pos = np.array([33.503363,-82.022313, 0])    # lat, lon, altitude (m)
rx_antenna = "Isotropic"                        # string for antenna type

rx_snr = calculations.calc_snr(fc,mod)          # Optimal RX SNR (dB) based on frequency and mode (shannon capacity)
# everything else is same across link budget

# specify detector information:
# detector will be a repeated array of rx_positions
# make it 100 steps between x and 100*y
dg_pos = calculations.detector_grid(tx_pos, rx_pos)

# perform calculations (friendly)
rx_loss_snr = calculations.path_loss(fc,tx_pos, tx_antenna, rx_pos, rx_antenna)
# this gets you GO/NOGO

print(f"LAT/LON/ALT: {tx_pos}")
print(f"Friendly LAT/LON/ALT: {rx_pos}")
print(f"MIN SNR: {rx_snr}")
print(f"PATH LOSS: {rx_loss_snr}")

if tx_pwr_db + rx_loss_snr > rx_snr:
    print("GO")
else:
    print("NOGO")

# range the enemy detector grid 
d_snr = 100 # arbitarily high
for i in range(len(dg_pos[0,:])):
    d_pos = dg_pos[:,i]
    if d_snr < rx_snr: # if the enemy can hear and intercept
        print(f"Enemy intercept as far away as: {d_pos}")
        break
    # find the snr of the received signal at the supposed enemy location
    d_snr = calculations.path_loss(fc,tx_pos, tx_antenna, d_pos, rx_antenna)