import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

data = pd.read_csv('sample_size_validation_results.csv')

elcc = data['ELCC'].values 
iterations = data['iterations'].values 
regions = data['region'].values


# plot
fig, ax = plt.subplots()

region_names = np.unique(regions)
for region in region_names:
    ax.scatter(iterations[regions == region],elcc[regions == region],alpha=.2)

ax.set_ylim([0,40])
ax.set_ylabel('ELCC')
ax.set_xlabel('MCS Sample Size')
ax.set_title('ELCC of 1 GW Solar in SLC, UT \n Sample Size Validation')

plt.legend([region.replace('[','').replace(']','').replace('\'','') for region in region_names])
plt.savefig('sample_size_validation')