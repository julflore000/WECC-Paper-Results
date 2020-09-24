import sys
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
from netCDF4 import Dataset 

def plot_single_map(ax, elcc_map, lats, lons, region, year, descriptor, capacity):
    """ Plot a single

    ...

    Args:
    ---------------
    `fig`

    `ax`

    `elcc_map`

    `lats`

    `lons`

    `region`

    `year`

    `descriptor`
    """
    stateList = ['all']

    # find ranges
    max_elcc = np.amax(elcc_map)
    min_elcc = np.amin(elcc_map)

    #vmax 
    vmax = int(max_elcc + (capacity-max_elcc)/3)

    #vmin
    vmin = int(min_elcc - (min_elcc)/3)

    print(max_elcc,min_elcc)
    print(vmax, vmin)

    # contour plot
    im = ax.imshow(elcc_map,vmax=vmax,vmin=vmin,cmap='plasma',origin='lower')
    cbar = ax.figure.colorbar(im,orientation='horizontal')
    #cbar.ax.set_ylabel('ELCC (MW)',fontsize=15)
    cbar.set_ticks(np.linspace(vmin,vmax,5)[1:-1])
    cbar.ax.set_yticklabels(np.linspace(vmin,vmax,5)[1:-1],fontsize=12)

    ax.set_xlabel('Longitude',fontsize=15)
    ax.set_ylabel('Latitude',fontsize=15)

    #find number of ticks
    num_ticks = np.arange(3,10)
    num_lats = 3
    num_lons = 3

    ax.set_xticks(np.linspace(0,len(lons)-1,num_lons))
    ax.set_yticks(np.linspace(0,len(lats)-1,num_lats))
    ax.set_yticklabels(np.linspace(lats[0],lats[-1],num_lats),fontsize=12)
    ax.set_xticklabels(np.linspace(lons[0],lons[-1],num_lons),fontsize=12)

    for i in range(len(lats)):
        for j in range(len(lons)):
            text = ax.text(j, i, str(int(elcc_map[i, j])),
                        ha="center", va="center", color="w")


    title = 'ELCC of\n'+descriptor+'\n'+region.capitalize()+' '+year

    ax.set_title(title,fontsize=18)

    return ax

def main():
    region = sys.argv[1]
    year = sys.argv[2]
    results_filename = sys.argv[3]
    img_filename = sys.argv[4]
    descriptor = sys.argv[5]

    # load results
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

    fig = plt.figure(figsize=(12,10))

    ax = fig.add_subplot(111)
    plot_single_map(ax, elcc_map, lats, lons, region, year, descriptor, 100)

    plt.savefig(img_filename,bbox_inches='tight',dpi=100)

if __name__ == "__main__":
    main()
