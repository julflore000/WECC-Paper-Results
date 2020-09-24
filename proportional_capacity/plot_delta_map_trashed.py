import sys
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
from netCDF4 import Dataset 
import matplotlib.colors as colors 
from plot_map import plot_single_map



def plot_dmap(region, elcc_map_1, elcc_map_2, lats, lons, img_filename, descriptor_1, descriptor_2,capacity):
    year = str(2018)
    elcc_map = elcc_map_2 - elcc_map_1

    fig = plt.figure(figsize=(10,36))

    # plot first
    ax1 = fig.add_subplot(311)
    ax1 = plot_single_map(ax1, elcc_map_1,lats,lons,region,year,descriptor_1,capacity)

    # plot second
    ax2 = fig.add_subplot(312)
    ax2 = plot_single_map(ax2, elcc_map_2,lats,lons,region,year,descriptor_2,capacity)

    # plot diff 
    ax3 = fig.add_subplot(313)
    # find ranges
    max_elcc = np.amax(elcc_map)
    min_elcc = np.amin(elcc_map)

    # contour plot
    biggest_diff = np.maximum(abs(max_elcc),abs(min_elcc))
    biggest_diff = np.maximum(biggest_diff,capacity*.15)

    divnorm = colors.TwoSlopeNorm(vmin=-1*abs(biggest_diff), vcenter=0, vmax=abs(biggest_diff))
    im = ax3.imshow(elcc_map,cmap='coolwarm',origin='lower',norm=divnorm)
    cbar = ax3.figure.colorbar(im,orientation='horizontal')
    #cbar.ax.set_ylabel('$\Delta$ ELCC (MW)',fontsize=15)
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


