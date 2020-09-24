from netCDF4 import Dataset 
import numpy as np 

d = Dataset('wecc_results.nc')

map_1 = d.variables['basin 2016 1 GW solar'][:]
map_2 = d.variables['basin 2016 1 GW solar 500 MW storage'][:]
map_3 = d.variables['basin 2016 100 MW solar'][:]

print(map_1.astype(int))
print(map_2.astype(int))
print(map_3.astype(int)-map_1.astype(int))