#import sys
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import re
from datetime import datetime
from scipy import stats

#filename1 = sys.argv[1]
#cpu_data = pd.read_csv(filename1)

cpu_data = pd.read_csv('sysinfo.csv')

# plt.figure(figsize=(12, 4))
# plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5)
# plt.show() # maybe easier for testing
# plt.savefig('cpu.svg') # for final submission

print(cpu_data)

filtered = stats.nonparametric.smoothers_lowess.lowess(cpu_data['temperature'].values, cpu_data['timestamp'])

print(filtered)