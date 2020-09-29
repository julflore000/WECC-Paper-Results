from plot_map import *
import matplotlib.pyplot as plt 
from netCDF4 import Dataset 

fig, axs = plt.subplots(5,2,figsize=(15,35),constrained_layout=True)
fig.suptitle('2018 Capacity Values by Region and Technology',fontsize=25)

d = Dataset('wecc_results.nc')

lats = d.variables['lat'][:]
lons = d.variables['lon'][:]

year = 2018
i = 0 
for region in ['basin','california','mountains','northwest','southwest']:
    for technology in ['solar', 'wind']:
        elcc_map = d.variables[region+' '+str(year)+' 1 GW '+technology][:]

        #plot 
        r = i//2
        c = i%2
        axs[r,c] = plot_single_map(axs[r,c],elcc_map,lats,lons,region,year,region.capitalize(),region.capitalize()+' 1 GW '+technology.capitalize())
        i += 1



plt.savefig('tmp_paper_fig_1')