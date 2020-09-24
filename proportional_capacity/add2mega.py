import numpy as np 
from netCDF4 import Dataset 
import pandas as pd 

def extract_map(results_filename):
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

    return elcc_map

def add_map(cdf, var_name, results_filename,capacity):
    cv = d.createVariable(var_name,'f4',('lat','lon',))
    #cv = d.variables[var_name]
    cv[:] = extract_map(results_filename)

# open cdf
d = Dataset('../wecc_results.nc', 'a')

# maps for 1 % solar/wind w/ and w/out .5% storage
# california
var_name = 'california 2018 1% solar'
filename = 'california_1_%_Solar_results.csv'
add_map(d,var_name, filename, 800)


var_name = 'california 2018 1% wind'
filename = 'california_1_%_Wind_results.csv'
add_map(d,var_name, filename, 800)

var_name = 'california 2018 1% solar .5% storage'
filename = 'california_1_%_Solar_.5_%_1_Hour_Storage_results.csv'
add_map(d,var_name, filename, 400+800)

var_name = 'california 2018 1% wind .5% storage'
filename = 'california_1_%_Wind_.5_%_1_Hour_Storage_results.csv'
add_map(d,var_name, filename, 400+800)

#mountains
var_name = 'mountains 2018 1% solar'
filename = 'mountains_1_%_Solar_results.csv'
add_map(d,var_name, filename, 220)


var_name = 'mountains 2018 1% wind'
filename = 'mountains_1_%_Wind_results.csv'
add_map(d,var_name, filename, 220)

var_name = 'mountains 2018 1% solar .5% storage'
filename = 'mountains_1_%_Solar_.5_%_1_Hour_Storage_results.csv'
add_map(d,var_name, filename, 110+220)

var_name = 'mountains 2018 1% wind .5% storage'
filename = 'mountains_1_%_Wind_.5_%_1_Hour_Storage_results.csv'
add_map(d,var_name, filename, 110+220)


# maps for 1 % storage
#cv = d.variables['california 2018 .5% storage (MW)']
#cv[:] = 71 * 400 / 100
#cv = d.variables['mountains 2018 .5% storage (MW)']
#cv[:] = 91 * 110 / 100


# close cdf
d.close()