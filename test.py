import sys
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from netCDF4 import Dataset 
import shapefile as shp  # Requires the pyshp package
from plot_map import plot_single_map
import seaborn as sns
import matplotlib.patches as mpatches
from scipy.stats import sem






#loading in data to correct dataframe
regions = ['california','basin','mountains','southwest','northwest']#,'','','','',]
yearList = ['2016','2017','2018']
subject = "1_GW_Wind_results"
masterDict = dict()
locationData = np.ones((3,342))
boxplotIndexFixData = dict()
seabornBoxplotData = pd.DataFrame(columns=['california','basin','mountains','southwest','northwest','year'])
mainYearsArray = (np.ones(342) * 2016.0)
mainYearsArray = np.append(mainYearsArray,(np.ones(342) * 2017.0))
mainYearsArray = np.append(mainYearsArray,(np.ones(342) * 2018.0))
seabornBoxplotData['year'] = seabornBoxplotData['year'].append(pd.Series(mainYearsArray))
seabornBoxplotData = seabornBoxplotData.replace(np.nan, 0)
uniqueLats = []
uniqueLons = []
#figure size for graphs
figureSize = [7.5,5]
#loading in by region and year, stores in location by year
for regionIndex, region in enumerate(regions):
    masterDict[region] = np.ones((3,342))
    boxplotIndexFixData[region] =  np.ones((4,342))
    boxplotIndexFixData[region][0] = np.nan
    yearArray = []
    for index,year in enumerate(yearList):
        filepath = "%s/%s/%s.csv" % (region,year,subject)
        data = pd.read_csv(filepath)
        data = data.sort_values(by=['latitude', 'longitude'])
        masterDict[region][index] = data["ELCC"]
        boxplotIndexFixData[region][index+1] = data["ELCC"]
        if index == 0:
            yearArray = data["ELCC"]
            if regionIndex == 0:
                uniqueLats = data['latitude']
                uniqueLons = data['longitude']
        else:
            yearArray = yearArray.append(data["ELCC"])
    seabornBoxplotData[region] = pd.Series(np.array(yearArray))








'''a = [1,2,3,4]


b= [5,6,7,8,0]

print(a[:] in b)
#sees if any of the indices are in that list
test = [value for value in a if(value in b)]
print(bool(test))'''
#getting rid of offshore values
rastData =  Dataset("offshore_bounds/offshoreBoundaries.nc")
tester = masterDict
#setting up values for raster data
latsRast =  np.array(rastData["lat"][:])
lonsRast =  np.array(rastData["lon"][:])
regionOfInterest = np.array(rastData["Band1"][:][:])
datapointsRemoved = 0
for lat,lon in zip(uniqueLats,uniqueLons):
    closestLatIndex = np.where( np.abs(latsRast-lat) == np.abs(latsRast-lat).min())[0][0]
    closestLonIndex = np.where( np.abs(np.abs(lonsRast)-np.abs(lon)) == np.abs(np.abs(lonsRast)-np.abs(lon)).min())[0][0]

        #if data is offshore get rid of it (set to nan)
    if (regionOfInterest[closestLatIndex][closestLonIndex] == 1):
        print(latsRast[closestLatIndex])
        print(lonsRast[closestLonIndex])
        latIndex = np.where(uniqueLats == lat)[0][0]
        lonIndex = np.where(uniqueLons == lon)[0][0]
#        if(latIndex == lonIndex):
        datapointsRemoved +=1
        for region in regions:
            for yearIndex in range(0,3):
                tester[region][yearIndex][latIndex] = np.nan

print(datapointsRemoved)
        
print(np.sum(tester[region][0] == np.nan))              
filtered_data = dict()
#filtering out nans now (ones that were offshore)
for regionIndex,region in enumerate(regions):
    newArrayLength = len(tester[region][0][~np.isnan(tester[region][0])])
    filtered_data[region] = np.ones((3,newArrayLength))
    for yearIndex,year in enumerate(yearList):
        filtered_data[region][yearIndex] = tester[region][yearIndex][~np.isnan(tester[region][yearIndex])]


yearList = ['2016','2017','2018']
labelList = (np.ones(len(regions)*3) * 2).tolist()
figureSize = [10,7.5]
plt.figure(figsize=(figureSize[0],figureSize[1]))
for index,region in enumerate(regions):
    print(region)
    if (index):
        labelList[index*3] = (" '16 ")#%s " %(region))
        labelList[index*3 +1] = (" '17 ")#%s " %(region))
        labelList[index*3+2] = (" '18 ")#%s " %(region))
        addList =  np.array([filtered_data[region][0],filtered_data[region][1],filtered_data[region][2]])
        boxplotData = np.concatenate((boxplotData, addList), axis=0)
    else:
        #inital list creation
        labelList[index*3] = (" '16 ")#%s " %(region))
        labelList[index*3 +1] = (" '17 ")#%s " %(region))
        labelList[index*3+2] = (" '18 ")#%s " %(region))
        boxplotData = np.array([filtered_data[region][0],filtered_data[region][1],filtered_data[region][2]])
    # Creating plot 
box = plt.boxplot(boxplotData.T,labels = labelList,showmeans = True,patch_artist= True)
plt.title("Change of %s across Years" % (subject.replace("_", " ")))
plt.xlabel("Year")
plt.ylabel("ELCC (%)")
colors = ['yellow', 'red', 'black', 'tan','blue']
colorIndex = -1
#filling in colors
handleList = []
for boxIndex, patch in enumerate(box['boxes']):
    if not (boxIndex  % 3):
        colorIndex += 1
        handle = mpatches.Patch(color=colors[colorIndex], label=regions[colorIndex])
        handleList.append(handle)
    patch.set_facecolor(colors[colorIndex])
meanLineHandle = mpatches.Patch(color='green', label="mean")
handleList.append(meanLineHandle)

plt.legend(handles=handleList,loc="upper right")#,fontsize ='small')
plt.show()