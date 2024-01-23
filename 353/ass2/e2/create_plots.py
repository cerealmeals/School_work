import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

filename1 = sys.argv[1]
filename2 = sys.argv[2]

file1 = pd.read_csv(filename1, sep=' ', header=None, index_col=1,
        names=['lang', 'page', 'views', 'bytes'])

file2 = pd.read_csv(filename2, sep=' ', header=None, index_col=1,
        names=['lang', 'page', 'views', 'bytes'])

print(file1)
print(file1.columns)
#print(file2)

sorted_file1 = file1['views'].sort_values(ascending=False)

file1.sort_values(['views'], ascending=False)

plt.figure(figsize=(10, 5)) # change the size to something sensible
plt.subplot(1, 2, 1) # subplots in 1 row, 2 columns, select the first
plt.plot(sorted_file1.values) # build plot 1
# plt.subplot(1, 2, 2) # ... and then select the second
# plt.plot(…) # build plot 2
plt.show()