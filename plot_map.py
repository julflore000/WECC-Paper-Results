import sys
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
from netCDF4 import Dataset 
import shapefile as shp  # Requires the pyshp package

def plot_single_map(ax, elcc_map, lats, lons, region, year, descriptor, label_activation = False):
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

    `label_activation`: (bool) default set to false and if set to true will label the squares with the respective values
    """

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
            x = [i[0] for i in shape.shape.points[:]] #- np.min(lons)
            y = [i[1] for i in shape.shape.points[:]] #- np.min(lats)
            plt.plot(x,y,color='black',linewidth=2)
        else:
            for regionPart in range(0,nparts):
                if regionPart < (nparts-1):
                    endIndex = shape.shape.parts[regionPart+1]
                else:
                    endIndex = npoints
                x = [i[0] for i in shape.shape.points[shape.shape.parts[regionPart]:endIndex]] #- np.min(lons)
                y = [i[1] for i in shape.shape.points[shape.shape.parts[regionPart]:endIndex]] #- np.min(lats)
                plt.plot(x,y,color='black',linewidth=2)

    #END generation of state bounds
    #########
    #plot figure range
    plt.xlim(np.min(lons),np.max(lons))
    plt.ylim(np.min(lats),np.max(lats))


    # find ranges
    max_elcc = np.amax(elcc_map)
    min_elcc = np.amin(elcc_map)

    #vmax 
    vmax = int(max_elcc + (100-max_elcc)/3)

    #vmin
    vmin = int(min_elcc - (min_elcc)/3)

    print(max_elcc,min_elcc)
    print(vmax, vmin)

    ##############
    #CHANGE FOR CONTOUR OR REGULAR HEATMAP WITH SQUARES

    # contour plot, extent overlays the heatmap onto the regular map
    #im = ax.contourf(elcc_map,vmax=vmax,vmin=vmin,cmap='plasma', extent = [np.min(lons),np.max(lons),np.min(lats),np.max(lats)])
    
    #regular boxplot
    im = ax.imshow(np.flip(elcc_map,axis=0),vmax=vmax,vmin=vmin,cmap='plasma', extent = [np.min(lons),np.max(lons),np.min(lats),np.max(lats)])    

    ##############

    cbar = ax.figure.colorbar(im)
    cbar.ax.set_ylabel('ELCC (% of Nameplate)',fontsize=15)

    #lets matplot automatically figure out how to plot can change if need be
    #cbar.set_ticklabels(values)
    #cbar.ax.set_yticklabels(values,fontsize=12)

    ax.set_xlabel('Longitude',fontsize=15)
    ax.set_ylabel('Latitude',fontsize=15)

    #finds number of ticks-IMPORTANT: currently left in but right now the ticks seem good, feel free to change though whatever you want with formating!
    '''
    num_ticks = np.arange(3,10)
    num_lats = np.amin(num_ticks[len(lons)%num_ticks == 0])
    num_lons = np.amin(num_ticks[len(lons)%num_ticks == 0])

    ax.set_xticks(np.linspace(0,len(lons)-1,num_lons))
    ax.set_yticks(np.linspace(0,len(lats)-1,num_lats))
    ax.set_yticklabels(np.linspace(lats[0],lats[-1],num_lats),fontsize=12)
    ax.set_xticklabels(np.linspace(lons[0],lons[-1],num_lons),fontsize=12)
    '''
    if label_activation:
        lon_increase = (np.max(lons) - np.min(lons)) / (2.0 * len(lons))
        lat_increase = (np.max(lats) - np.min(lats)) / (2.0 * len(lats))

        lon_positions = np.linspace(start= np.min(lons), stop=np.max(lons), num=len(lons), endpoint=False)
        lat_positions = np.linspace(start= np.min(lats), stop=np.max(lats), num=len(lats), endpoint=False)

        #flipped for text plotting
        #putting values in for boxes
        for lat_index, lat in enumerate(lat_positions):
            for lon_index, lon in enumerate(lon_positions):
                label = elcc_map[lat_index, lon_index]
                text_lon = lon + lon_increase
                text_lat = lat + lat_increase
                ax.text(text_lon, text_lat, label, color='w', ha='center', va='center')

 
    title = 'ELCC of\n'+descriptor+'\n'+region.capitalize() +' '+year

    ax.set_title(title,fontsize=18)

    return ax


def main():

    #for testing
    '''
    region = "california"
    year = '2016'
    results_directory = region+'/'+year+'/'
    results_filename = results_directory + "1_GW_Solar_results.csv"
    img_filename = results_directory+'map_1_GW_Solar'
    descriptor = '1 GW Solar'

    '''
    region = sys.argv[1]
    year = sys.argv[2]
    results_filename = sys.argv[3]
    img_filename = sys.argv[4]
    descriptor = sys.argv[5]

    #change label activation here to write values to boxes or not
    label_activation = True
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

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111)
    
    #actually plot ELCC values
    plot_single_map(ax, elcc_map, lats, lons, region, year, descriptor,label_activation)
    plt.savefig(img_filename,bbox_inches='tight',dpi=100)

if __name__ == "__main__":
    main()
