from netCDF4 import Dataset 
import numpy as np 

d = Dataset('WECC_Results.nc')

map_1 = d.variables['basin 2016 1 GW solar'][:]
map_2 = d.variables['basin 2016 1 GW solar 500 MW storage'][:]

print(map_1.astype(int))
print(map_2.astype(int))
print(map_2.astype(int)-map_1.astype(int))