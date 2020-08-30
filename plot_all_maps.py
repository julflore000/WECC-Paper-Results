import sys
import os

region = sys.argv[1]
year = sys.argv[2]
# find results folder
results_directory = region+'/'+year+'/'

# parameters

os.system('python plot_map.py ' #main program run
            +region+' '+year+' '
            +results_directory+'1_GW_Solar_results.csv' # results file
            +' '+results_directory+'map_1_GW_Solar' #output name
            +' '+'"'+'1 GW Solar' #descriptor
            +'"')

os.system('python plot_map.py '
            +region+' '+year+' '
            +results_directory+'1_GW_Wind_results.csv' # results file
            +' '+results_directory+'map_1_GW_Wind' #output name
            +' '+'"'+'1 GW Wind' #descriptor
            +'"')

os.system('python plot_map.py '
            +region+' '+year+' '
            +results_directory+'100_MW_Solar_results.csv' # results file
            +' '+results_directory+'map_100_MW_Solar' #output name
            +' '+'"'+'100 MW Solar' #descriptor
            +'"')

os.system('python plot_map.py '
            +region+' '+year+' '
            +results_directory+'100_MW_Wind_results.csv' # results file
            +' '+results_directory+'map_100_MW_Wind' #output name
            +' '+'"'+'100 MW Wind' #descriptor
            +'"')

os.system('python plot_map.py '
            +region+' '+year+' '
            +results_directory+'5_GW_Solar_results.csv' # results file
            +' '+results_directory+'map_5_GW_Solar' #output name
            +' '+'"'+'5 GW Solar' #descriptor
            +'"')

os.system('python plot_map.py '
            +region+' '+year+' '
            +results_directory+'5_GW_Wind_results.csv' # results file
            +' '+results_directory+'map_5_GW_Wind' #output name
            +' '+'"'+'5 GW Wind' #descriptor
            +'"')

os.system('python plot_map.py '
            +region+' '+year+' '
            +results_directory+'1_GW_Solar_500_MW_1_Hour_Storage_results.csv' # results file
            +' '+results_directory+'map_1_GW_Solar_500_MW_1_Hour_Storage' #output name
            +' '+'"'+'1 GW Solar + 500 MW 1 Hour Storage' #descriptor
            +'"')

os.system('python plot_map.py '
            +region+' '+year+' '
            +results_directory+'1_GW_Wind_500_MW_1_Hour_Storage_results.csv' # results file
            +' '+results_directory+'map_1_GW_Wind_500_MW_1_Hour_Storage' #output name
            +' '+'"'+'1 GW Wind + 500 MW 1 Hour Storage' #descriptor
            +'"')

os.system('python plot_map.py '
            +region+' '+year+' '
            +results_directory+'1_GW_Solar_2x_Renewables_results.csv' # results file
            +' '+results_directory+'map_1_GW_Solar_2x_Renewables' #output name
            +' '+'"'+'1 GW Solar w/ 2x Existing Renewables' #descriptor
            +'"')

os.system('python plot_map.py '
            +region+' '+year+' '
            +results_directory+'1_GW_Wind_2x_Renewables_results.csv' # results file
            +' '+results_directory+'map_1_GW_Wind_2x_Renewables' #output name
            +' '+'"'+'1 GW Wind w/ 2x Existing Renewables' #descriptor
            +'"')

# delta maps
os.system('python plot_delta_map.py '
            +region+' '+year+' '
            +results_directory+'1_GW_Solar_results.csv' # results file 1
            +' '+results_directory+'100_MW_Solar_results.csv' # results file 2
            +' '+results_directory+'map_delta_'+'1_GW_Solar_to_100_MW_Solar' #image filename
            +' "'+'1 GW Solar' # descriptor results 1
            +'" "'+'100 MW Solar' #descriptor results 2
            +'"')

os.system('python plot_delta_map.py '
            +region+' '+year+' '
            +results_directory+'1_GW_Wind_results.csv' # results file 1
            +' '+results_directory+'100_MW_Wind_results.csv' # results file 2
            +' '+results_directory+'map_delta_'+'1_GW_Wind_to_100_MW_Wind' #image filename
            +' "'+'1 GW Wind' # descriptor results 1
            +'" "'+'100 MW Wind' #descriptor results 2
            +'"')

os.system('python plot_delta_map.py '
            +region+' '+year+' '
            +results_directory+'1_GW_Solar_results.csv' # results file 1
            +' '+results_directory+'5_GW_Solar_results.csv' # results file 2
            +' '+results_directory+'map_delta_'+'1_GW_Solar_to_5_GW_Solar' #image filename
            +' "'+'1 GW Solar' # descriptor results 1
            +'" "'+'5 GW Solar' #descriptor results 2
            +'"')

os.system('python plot_delta_map.py '
            +region+' '+year+' '
            +results_directory+'1_GW_Wind_results.csv' # results file 1
            +' '+results_directory+'5_GW_Wind_results.csv' # results file 2
            +' '+results_directory+'map_delta_'+'1_GW_Wind_to_5_GW_Wind' #image filename
            +' "'+'1 GW Wind' # descriptor results 1
            +'" "'+'5 GW Wind' #descriptor results 2
            +'"')

os.system('python plot_delta_map.py '
            +region+' '+year+' '
            +results_directory+'1_GW_Solar_results.csv' # results file 1
            +' '+results_directory+'1_GW_Solar_500_MW_1_Hour_Storage_results.csv' # results file 2
            +' '+results_directory+'map_delta_'+'1_GW_Solar_to_1_GW_Solar_500_MW_1_Hour_Storage' #image filename
            +' "'+'1 GW Solar' # descriptor results 1
            +'" "'+'1 GW Solar + 500 MW 1 Hour Storage' #descriptor results 2
            +'"')

os.system('python plot_delta_map.py '
            +region+' '+year+' '
            +results_directory+'1_GW_Wind_results.csv' # results file 1
            +' '+results_directory+'1_GW_Wind_500_MW_1_Hour_Storage_results.csv' # results file 2
            +' '+results_directory+'map_delta_'+'1_GW_Wind_to_1_GW_Wind_500_MW_1_Hour_Storage' #image filename
            +' "'+'1 GW Wind' # descriptor results 1
            +'" "'+'1 GW Wind + 500 MW 1 Hour Storage' #descriptor results 2
            +'"')

os.system('python plot_delta_map.py '
            +region+' '+year+' '
            +results_directory+'1_GW_Solar_results.csv' # results file 1
            +' '+results_directory+'1_GW_Solar_2x_Renewables_results.csv' # results file 2
            +' '+results_directory+'map_delta_'+'1_GW_Solar_to_1_GW_Solar_2x_Renewable' #image filename
            +' "'+'1 GW Solar' # descriptor results 1
            +'" "'+'1 GW Solar w/ 2x Existing Renewables' #descriptor results 2
            +'"')

os.system('python plot_delta_map.py '
            +region+' '+year+' '
            +results_directory+'1_GW_Wind_results.csv' # results file 1
            +' '+results_directory+'1_GW_Wind_2x_Renewables_results.csv' # results file 2
            +' '+results_directory+'map_delta_'+'1_GW_Wind_to_1_GW_Wind_2x_Renewable' #image filename
            +' "'+'1 GW Wind' # descriptor results 1
            +'" "'+'1 GW Wind w/ 2x Existing Renewables' #descriptor results 2
            +'"')



