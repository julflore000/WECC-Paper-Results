import numpy as np 
import sys 

region = sys.argv[1]

risk = np.loadtxt(region+'_hourly_risk.csv').astype(float)

num_hours = 20
hours = np.flip(np.argsort(risk))[:num_hours]
risk = np.flip(np.sort(risk))[:num_hours]
print('month:',hours // 24 // 30 + 1)
print('day:',hours // 24 + 1)
print('hour:',hours % 24)
print('hour of year:',hours)
print('risk:',risk)


