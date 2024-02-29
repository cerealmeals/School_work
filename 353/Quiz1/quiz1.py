import numpy as np
import pandas as pd

df = pd.DataFrame({
    'a':[2,3,4,5,6],
    'b':[1.0, 2.0,3.0, 4.0]
}) 

print(df['a']+df['b'])

df1 = pd.DataFrame({'lkey': ['foo', 'bar', 'baz', 'foo'],

                    'value': [1, 2, 3, 5]})

df2 = pd.DataFrame({'rkey': ['foo', 'bar', 'baz', 'foo'],

                    'value': [5, 6, 7, 8]})

print(df1)