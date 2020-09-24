from netCDF4 import Dataset 
import pandas as pd 
import numpy as np


# sample map

sample = pd.read_csv('basin/2016/1_GW_Solar_results.csv',index_col=0)

latitude = sample['latitude'].values.astype(float)
longitude = sample['longitude'].values.astype(float)

lats = np.unique(latitude).flatten()
lons = np.unique(longitude).flatten()

print(lats,lons)

# create cdf
d = Dataset('wecc_results.nc','w')
lat = d.createDimension('lat',len(lats))
lon = d.createDimension('lon',len(lons))
lat = d.createVariable('lat','f4',('lat',))
lon = d.createVariable('lon','f4',('lon',))
lat[:] = lats
lon[:] = lons

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

def add_map(cdf, var_name, results_filename):
    cv = d.createVariable(var_name,'f4',('lat','lon',))
    cv[:] = extract_map(results_filename)


for region in ['basin','california','mountains','northwest','southwest']:
    for year in ['2016','2017','2018']:
        for generator_size in ['100 MW','1 GW','5 GW']:
            for technology in ['solar','wind']:

                var_name = region+' '+year+' '+generator_size+' '+technology
                results_filename = region+'/'+year+'/'+generator_size.replace(' ','_')+'_'+technology.capitalize()+'_results.csv'

                add_map(d, var_name, results_filename)

                #sensitivities
                if generator_size == '1 GW':

                    #storage
                    var_name = region+' '+year+' '+generator_size+' '+technology+' 500 MW storage'
                    results_filename = region+'/'+year+'/'+'1_GW_'+technology.capitalize()+'_500_MW_1_Hour_Storage_results.csv'
                    add_map(d, var_name, results_filename)

                    #double renewables
                    var_name = region+' '+year+' '+generator_size+' '+technology+' 2x renewables'
                    results_filename = region+'/'+year+'/'+'1_GW_'+technology.capitalize()+'_2x_Renewables_results.csv'
                    add_map(d, var_name, results_filename)

d.close()



                
                
                

