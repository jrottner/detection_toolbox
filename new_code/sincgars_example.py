import numpy as np
import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
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
d_pos = tx_pos
for i in range(len(dg_pos[0,:])):
    if d_snr < rx_snr: # if the enemy can hear and intercept
        print(f"Enemy intercept as far away as: {d_pos}")
        break
    d_pos = dg_pos[:,i]
    # find the snr of the received signal at the supposed enemy location
    d_snr = calculations.path_loss(fc,tx_pos, tx_antenna, d_pos, rx_antenna)

# recalculate snr
heatmap_pos = calculations.heatmap(tx_pos, rx_pos)
dg_snr = np.zeros_like(heatmap_pos[:,:,0])

for i in range(len(dg_snr[1,:])): # lon
    for j in range(len(dg_snr[0,:])): # lat
        dg_snr[j,i] = calculations.path_loss(fc,tx_pos, tx_antenna, heatmap_pos[i,j,:], rx_antenna)

# plot it
dir_path = os.path.dirname(os.path.realpath(__file__))
county_filename = dir_path + '/county_shapes/countyl010g.shp'
reader = shpreader.Reader(county_filename)

counties = list(reader.geometries())

COUNTIES = cfeature.ShapelyFeature(counties, ccrs.PlateCarree())

plt.figure(figsize=(10, 6))
ax = plt.axes(projection=ccrs.PlateCarree())

ax.add_feature(cfeature.LAND.with_scale('50m'))
ax.add_feature(cfeature.OCEAN.with_scale('50m'))
ax.add_feature(cfeature.LAKES.with_scale('50m'))
ax.add_feature(COUNTIES, facecolor='none', edgecolor='gray')

ax.coastlines('50m')

ax.set_extent([-81, -83, 32, 34 ], crs=ccrs.PlateCarree())
ax.coastlines(resolution='50m')
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
plt.plot([tx_pos[1], rx_pos[1]], [tx_pos[0], rx_pos[0]],
         color='blue', linewidth=2, marker='o',
         transform=ccrs.Geodetic(),
         )

plt.plot([tx_pos[1], rx_pos[1]], [tx_pos[0], rx_pos[0]],
         color='gray', linestyle='--',
         transform=ccrs.PlateCarree(),
         )

plt.text(tx_pos[1] - 0.01, tx_pos[0] - 0.01, 'TX POS',
         horizontalalignment='right',
         transform=ccrs.Geodetic())

plt.text(rx_pos[1] + 0.01, rx_pos[0] + 0.01, 'RX POS',
         horizontalalignment='left',
         transform=ccrs.Geodetic())

plt.contourf(heatmap_pos[:,:,1], heatmap_pos[:,:,0], dg_snr, 30,
             transform=ccrs.PlateCarree())

plt.show()