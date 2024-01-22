import sys
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

filename1 = sys.argv[1]
filename2 = sys.argv[2]

file1 = pd.read_csv(filename1, sep=' ', header=None, index_col=1,
        names=['lang', 'page', 'views', 'bytes'])

file2 = pd.read_csv(filename2, sep=' ', header=None, index_col=1,
        names=['lang', 'page', 'views', 'bytes'])

print(file1)
print(file2)