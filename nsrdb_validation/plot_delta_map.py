import sys
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
from netCDF4 import Dataset 
import matplotlib.colors as colors 
#from plot_map import plot_single_map

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
print(np.average(elcc_map))
print(np.average(np.absolute(elcc_map)))

