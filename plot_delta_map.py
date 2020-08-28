import sys
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
from netCDF4 import Dataset 
import matplotlib.colors as colors 
from plot_map import plot_single_map

# difference between filename 1 and 2
region = sys.argv[1]
year = sys.argv[2]
results_filename_1 = sys.argv[3]
results_filename_2 = sys.argv[4]
img_filename = sys.argv[5]
descriptor_1 = sys.argv[6]
descriptor_2 = sys.argv[7]

# load results

def get_elcc_map(results_filename, **kwargs):

    results = pd.read_csv(results_filename,index_col=0)

    latitude = results['latitude'].values.astype(float)
    longitude = results['longitude'].values.astype(float)
    elcc = results['ELCC'].values.astype(int)

    # make map 

    lats = np.unique(latitude)
    lons = np.unique(longitude)

    elcc_map = np.zeros((len(lats),len(lons)))

    # fill map

    for i in range(len(elcc)):
        
        elcc_map[np.argwhere(lats == latitude[i])[0,0], np.argwhere(lons == longitude[i])[0,0]] = elcc[i]

    if "return_lat_lons" in kwargs:
        if kwargs["return_lat_lons"]:
            return elcc_map, lats, lons

    return elcc_map

elcc_map_1,lats,lons = get_elcc_map(results_filename_1,return_lat_lons=True)
elcc_map_2 = get_elcc_map(results_filename_2)
elcc_map = elcc_map_2 - elcc_map_1

fig = plt.figure(figsize=(36,10))

# plot first
ax1 = fig.add_subplot(131)
ax1 = plot_single_map(ax1, elcc_map_1,lats,lons,region,year,descriptor_1)

# plot second
ax2 = fig.add_subplot(132)
ax2 = plot_single_map(ax2, elcc_map_2,lats,lons,region,year,descriptor_2)

# plot diff 
ax3 = fig.add_subplot(133)
# find ranges
max_elcc = np.amax(elcc_map)
min_elcc = np.amin(elcc_map)

# contour plot
biggest_diff = np.maximum(abs(max_elcc),abs(min_elcc))
biggest_diff = np.maximum(biggest_diff,15)

divnorm = colors.TwoSlopeNorm(vmin=-1*abs(biggest_diff), vcenter=0, vmax=abs(biggest_diff))
im = ax3.imshow(elcc_map,cmap='coolwarm',origin='lower',norm=divnorm)
cbar = ax3.figure.colorbar(im)
cbar.ax.set_ylabel('$\Delta$ ELCC',fontsize=15)
cbar.set_ticks(np.linspace(-biggest_diff,biggest_diff,3))


ax3.set_xlabel('Longitude',fontsize=15)
ax3.set_ylabel('Latitude',fontsize=15)

ax3.set_xticks(np.linspace(0,len(lons)-1,3))
ax3.set_yticks(np.linspace(0,len(lats)-1,3))
ax3.set_yticklabels(np.linspace(lats[0],lats[-1],3),fontsize=12)
ax3.set_xticklabels(np.linspace(lons[0],lons[-1],3),fontsize=12)


for i in range(len(lats)):
    for j in range(len(lons)):
        text = ax3.text(j, i, str(int(elcc_map[i, j])),
                       ha="center", va="center", color="w")


title = '$\Delta$ of ELCC from\n'+descriptor_1+' to '+descriptor_2+'\n'+region.capitalize()+' '+year

ax3.set_title(title,fontsize=18)

plt.savefig(img_filename,bbox_inches='tight',dpi=100)


