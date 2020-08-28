import numpy as np
import sys
import pandas as pd 
import matplotlib.pyplot as plt 
from netCDF4 import Dataset
from elcc_impl import get_hourly_load, get_total_interchange


def main():
    year = 2016
    region = sys.argv[1]
    descriptor = '\n'+ region.capitalize() + ' ' + str(year)

    # Get BAs

    TEPPC_regions = pd.read_csv('../demand/_regions.csv').fillna('nan')

    regions = TEPPC_regions[region.capitalize()].values.flatten().astype(str)
    regions = np.unique(regions[regions != 'nan'])

    # Get data

    load = get_hourly_load(year, regions)
    interchange = get_total_interchange(year,regions,'../total_interchange/')
    total = load + interchange

    # Analyze

    if True:
        #annual/seasonal averages by time of day
        annual_hourly_load_average = np.zeros(24)
        summer_hourly_load_average = np.zeros(24)
        winter_hourly_load_average = np.zeros(24)
        annual_hourly_average = np.zeros(24)
        summer_hourly_average = np.zeros(24)
        winter_hourly_average = np.zeros(24)
        for hr in range(24):
            annual_hourly_load_average[hr] = np.average(load[hr::24])
            summer_hourly_load_average[hr] = np.average(load[2190-6+hr:8760-2190+6:24])
            winter_hourly_load_average[hr] = np.average(np.append(load[hr:2190-6:24],load[8760-2190+6+hr::24]))
            annual_hourly_average[hr] = np.average(total[hr::24])
            summer_hourly_average[hr] = np.average(total[2190-6+hr:8760-2190+6:24])
            winter_hourly_average[hr] = np.average(np.append(total[hr:2190-6:24],total[8760-2190+6+hr::24]))
        
        fig = plt.figure(figsize=(18,7))
        ax1 = fig.add_subplot(131)
        ax2 = fig.add_subplot(132)
        ax3 = fig.add_subplot(133)

        ax1.plot(annual_hourly_load_average)
        ax1.plot(annual_hourly_average)
        ax2.plot(summer_hourly_load_average)
        ax2.plot(summer_hourly_average)
        ax3.plot(winter_hourly_load_average)
        ax3.plot(winter_hourly_average)

        ax1.set_ylabel('MW')

        for ax in [ax1, ax2, ax3]:
            ax.legend(['Load','Load w/ Interchange'])
            ax.set_ylim(np.minimum(np.amin(load),np.amin(total)),
                        np.maximum(np.amax(load),np.amax(total)))
            ax.set_xlim([0,24])
            ax.set_xlabel('Hour of Day')

        ax1.set_title('Annual Average Demand by Time of Day'+descriptor)
        ax2.set_title('Summer Average Demand by Time of Day'+descriptor)
        ax3.set_title('Winter Average Demand by Time of Day'+descriptor)
        
        plt.savefig('demand_by_hour_'+region+'_'+str(year))

    if True:
        #  two highest risk days
        start_hour = int(sys.argv[2])
        end_hour = start_hour + 48
        timeframe = range(start_hour,end_hour)

        # get generation
        cf = Dataset('../wecc_powGen/2016_solar_generation_cf.nc').variables['cf'][:]

        # get risk
        risk = np.loadtxt(region+'_hourly_risk.csv') 

        fig = plt.figure(figsize=(10,8))
        ax = fig.add_subplot(111)
        ax2 = ax.twinx()

        ax2.plot(cf[0,0],lw=2)
        ax2.plot(cf[0,-1],lw=2)
        ax2.plot(cf[-1,-1],lw=2)
        ax2.plot(cf[-1,0],lw=2)
        ax2.scatter(range(8760),risk,marker='x',s=10)

        ax.plot(total,color='#aa0000',lw=4)

        ax.set_xlim([start_hour,end_hour])

        ax.legend(['Load'])
        ax2.legend(['Southwestern Corner','Southeastern Corner','Northeastern Corner','Northwestern Corner','Hourly Risk'])
        
        ax.set_ylabel('MW')
        ax2.set_ylabel('Capacity Factor/Risk')
        ax.set_xlabel('Hour of Year')

        ax.set_title('Highest Risk Day 48-Hour Horizon'+descriptor)

        plt.savefig('highest_risk_'+region+'_'+str(year))

        
        

if __name__ == "__main__":
    main()