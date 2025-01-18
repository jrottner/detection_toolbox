import numpy as np
import matplotlib.pyplot as plt
import calculations
import pandas as pd
import os

'''
key_val = 10
npoints = 100
x = key_val * np.arange(npoints)

y = key_val * np.logspace(-1,1,npoints)


tx_pos = np.array([33.420732,-82.143516,0]) 
rx_pos = np.array([33.503363,-82.022313, 0])

heatmap_pos = calculations.heatmap(tx_pos, rx_pos)



import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader


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
for i in range(len(heatmap_pos[:,0,0])):
    for j in range(len(heatmap_pos[0,:,0])):
        plt.plot([tx_pos[1], heatmap_pos[i,j,1]], [tx_pos[0], heatmap_pos[i,j,0]],
                color='blue', linewidth=2, marker='o',
                transform=ccrs.Geodetic(),
                )

plt.show()
'''
dir_path = os.path.dirname(os.path.realpath(__file__))
df = pd.read_csv(dir_path + '/ant_data/EIRP_Data.csv')

# csv is sorted as theta, phi, power
# take only theta=0 values
power1d = df['Power'].head(73)
power1d = np.array(power1d)

# interp
npoints = 100
yagi_pattern = np.zeros((2,npoints))
yagi_pattern[0,:] = np.linspace(0,2*np.pi,npoints)
yagi_pattern[1,:] =  1 - 1 * np.sin(yagi_pattern[0,:] - np.pi/2)

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.plot(yagi_pattern[0,:], yagi_pattern[1,:])

plt.show()