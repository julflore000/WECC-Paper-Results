import sys
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
from netCDF4 import Dataset 
import shapefile as shp  # Requires the pyshp package
from plot_map import plot_single_map













def main(fileName):
    """ 
    Plots that specific type (e.g. "1_GW_Solar_Storage") across all regions and years and averages

    ...

    Args:
    ---------------
    `fig`

    `ax`
    """
    regions = ["california","mountains","northwest","southwest","basin"]
    master_elcc_map = np.zeros((18,15))
    timesThru = 0
    for region in regions:
        for year in ['2016','2017','2018']:
            results_directory = region+'/'+year+'/'
            results_filename = results_directory + fileName + ".csv"
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
            
            #add on to total map
            timesThru +=1
            master_elcc_map += elcc_map
    
    print(timesThru)
    master_elcc_map = master_elcc_map / 15
    
    #now plotting
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111)                
    plot_single_map(ax, elcc_map, lats, lons, region, year, fileName,True,True)
    plt.show()
main("100_MW_Wind_results")
