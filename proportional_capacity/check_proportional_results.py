from netCDF4 import Dataset 
import matplotlib.pyplot as plt 
import matplotlib.colors as colors 
import numpy as np
from plot_delta_map_trashed import *

def load_region(region,capacity):
    d = Dataset('../wecc_results.nc')
    a = dict()
    a['solar'] = d.variables[region+' 2018 1% solar (MW)'][:].astype(int)
    a['wind'] = d.variables[region+' 2018 1% wind (MW)'][:].astype(int)
    a['storage'] = d.variables[region+' 2018 .5% storage (MW)'][:].astype(int)
    a['solar storage'] = d.variables[region+' 2018 1% solar .5% storage (MW)'][:].astype(int)
    a['wind storage'] = d.variables[region+' 2018 1% wind .5% storage (MW)'][:].astype(int)
    a['solar storage (%)'] = d.variables[region+' 2018 1% solar .5% storage'][:].astype(int)
    a['wind storage (%)'] = d.variables[region+' 2018 1% wind .5% storage'][:].astype(int)
    a['1 GW solar'] = d.variables[region+' 2018 1 GW solar'][:].astype(int)
    a['1 GW wind'] = d.variables[region+' 2018 1 GW wind'][:].astype(int)
    a['1 GW solar 500 MW storage'] = d.variables[region+' 2018 1 GW solar 500 MW storage'][:].astype(int)
    a['1 GW wind 500 MW storage'] = d.variables[region+' 2018 1 GW wind 500 MW storage'][:].astype(int)

    # solar/storage
    plot_dmap(region, a['solar']+a['storage'],a['solar storage'],d.variables['lat'][:],d.variables['lon'][:],region+'_solar_storage_contribution','ELCC 1% Solar + ELCC .5% Storage','1% Solar and .5% Storage',1.5*capacity)

    # wind/storage
    plot_dmap(region, a['wind']+a['storage'],a['wind storage'],d.variables['lat'][:],d.variables['lon'][:],region+'_wind_storage_contribution','ELCC 1% Wind + ELCC .5% Storage','1% Wind and .5% Storage',1.5*capacity)

    # compare with larger generator solar
    plot_dmap(region, a['solar storage (%)'],a['1 GW solar 500 MW storage'],d.variables['lat'][:],d.variables['lon'][:],region+'_proportional_solar_storage_contribution','1% Solar and .5% Storage','1 GW Solar and 500 MW Storage',100)

    # compare with larger generator wind
    plot_dmap(region, a['wind storage (%)'],a['1 GW wind 500 MW storage'],d.variables['lat'][:],d.variables['lon'][:],region+'_proportional_wind_storage_contribution','1% Wind and .5% Storage','1 GW Wind and 500 MW Storage',100)

    return a

def main():
    load_region('california',800)
    load_region('mountains',220)

if __name__ == "__main__":
    main()