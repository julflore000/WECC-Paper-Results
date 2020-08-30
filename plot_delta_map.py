import sys
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
from netCDF4 import Dataset 
import matplotlib.colors as colors 
from plot_map import plot_single_map
import shapefile as shp  # Requires the pyshp package

# difference between filename 1 and 2
region = sys.argv[1]
year = sys.argv[2]
results_filename_1 = sys.argv[3]
results_filename_2 = sys.argv[4]
img_filename = sys.argv[5]
descriptor_1 = sys.argv[6]
descriptor_2 = sys.argv[7]

#to display values of boxes or contour plot
label_activation = True


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
ax1 = plot_single_map(ax1, elcc_map_1,lats,lons,region,year,descriptor_1,label_activation)

# plot second
ax2 = fig.add_subplot(132)
ax2 = plot_single_map(ax2, elcc_map_2,lats,lons,region,year,descriptor_2,label_activation)

# plot diff 
ax3 = fig.add_subplot(133)

######
#GENERATING STATE BOUNDS
#need to shift a little bit for 1/2 size resolution, if heatmap and lines not adding up adjust this parameter
#latShift = .5
#lonShift = .3125

sf = shp.Reader("state_lines\cb_2018_us_state_500k\cb_2018_us_state_500k.shp")

for shape in sf.shapeRecords():
    npoints=len(shape.shape.points) # total points
    nparts = len(shape.shape.parts) # total parts

    if nparts == 1:
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        plt.plot(x,y,color='black',linewidth=2)
    else:
        for regionPart in range(0,nparts):
            if regionPart < (nparts-1):
                endIndex = shape.shape.parts[regionPart+1]
            else:
                endIndex = npoints
            x = [i[0] for i in shape.shape.points[shape.shape.parts[regionPart]:endIndex]]
            y = [i[1] for i in shape.shape.points[shape.shape.parts[regionPart]:endIndex]]
            plt.plot(x,y,color='black',linewidth=2)

#END generation of state bounds
#########




# find ranges
max_elcc = np.amax(elcc_map)
min_elcc = np.amin(elcc_map)

# contour plot
biggest_diff = np.maximum(abs(max_elcc),abs(min_elcc))
biggest_diff = np.maximum(biggest_diff,15)

divnorm = colors.TwoSlopeNorm(vmin=-1*abs(biggest_diff), vcenter=0, vmax=abs(biggest_diff))
##############
#CHANGE FOR CONTOUR OR REGULAR HEATMAP WITH SQUARES comment out whichever plot you dont want!!

# contour plot, extent overlays the heatmap onto the regular map
#im = ax3.contourf(elcc_map,cmap='coolwarm',extent = [np.min(lons),np.max(lons),np.min(lats),np.max(lats)],norm=divnorm)

#regular boxplot 
im = ax3.imshow(np.flip(elcc_map,axis=0),cmap='coolwarm', extent = [np.min(lons),np.max(lons),np.min(lats),np.max(lats)],norm=divnorm)

##############

cbar = ax3.figure.colorbar(im)
cbar.ax.set_ylabel('$\Delta$ ELCC',fontsize=15)

#lets matplot automatically figure out how to plot can change if need be
#cbar.set_ticks(np.linspace(-biggest_diff,biggest_diff,3))


ax3.set_xlabel('Longitude',fontsize=15)
ax3.set_ylabel('Latitude',fontsize=15)

#finds number of ticks-IMPORTANT: currently left in but right now the ticks seem good, feel free to change though whatever you want with formating!
'''
ax3.set_xticks(np.linspace(0,len(lons)-1,3))
ax3.set_yticks(np.linspace(0,len(lats)-1,3))
ax3.set_yticklabels(np.linspace(lats[0],lats[-1],3),fontsize=12)
ax3.set_xticklabels(np.linspace(lons[0],lons[-1],3),fontsize=12)


for i in range(len(lats)):
    for j in range(len(lons)):
        text = ax3.text(j, i, str(int(elcc_map[i, j])),
                       ha="center", va="center", color="w")
'''

if label_activation:
        lon_increase = (np.max(lons) - np.min(lons)) / (2.0 * len(lons))
        lat_increase = (np.max(lats) - np.min(lats)) / (2.0 * len(lats))

        lon_positions = np.linspace(start= np.min(lons), stop=np.max(lons), num=len(lons), endpoint=False)
        lat_positions = np.linspace(start= np.min(lats), stop=np.max(lats), num=len(lats), endpoint=False)

        #flipped for text plotting
        #flipped_elcc_map = np.flip(elcc_map,axis=0)
        #putting values in for boxes
        for lat_index, lat in enumerate(lat_positions):
            for lon_index, lon in enumerate(lon_positions):
                label = elcc_map[lat_index, lon_index]
                text_lon = lon + lon_increase
                text_lat = lat + lat_increase
                ax3.text(text_lon, text_lat, label, color='w', ha='center', va='center')


title = '$\Delta$ of ELCC from\n'+descriptor_1+' to '+descriptor_2+'\n'+region.capitalize()+' '+year

ax3.set_title(title,fontsize=18)
#fix figure range
plt.xlim(np.min(lons),np.max(lons))
plt.ylim(np.min(lats),np.max(lats))
plt.savefig(img_filename,bbox_inches='tight',dpi=100)


