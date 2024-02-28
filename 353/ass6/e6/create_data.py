import time
from implementations import all_implementations
import numpy as np
import pandas as pd

df = pd.DataFrame(columns=['type', 'time'])
for i in range(100):
    arr = np.random.randint(3000, size=300)
    for sort in all_implementations:
        st = time.time()
        res = sort(arr)
        en = time.time()
        duration = en - st
        df.loc[len(df.index)] = [sort.__name__, duration]
print(df)
df.to_csv('data.csv', index=False)
print('done')
