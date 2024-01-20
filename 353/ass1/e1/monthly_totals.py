import pandas as pd
import numpy as np

def date_to_month(d):
    # You may need to modify this function, depending on your data types.
    list = d.split('-')
    return list[0] + '-' + list[1]

def pivot_months_pandas(data):
    """
    Create monthly precipitation totals for each station in the data set.
    
    This should use Pandas methods to manipulate the data.
    """
    # ...
    data['month'] = data['date'].map(lambda x: date_to_month(x))
    
    monthly = data.groupby(by=['name', 'month']).agg({'precipitation' : ['sum']}).reset_index()
    monthly['sum'] = monthly['precipitation']
    monthly = monthly.pivot(index='name', columns='month', values='sum')

    counts = data.groupby(by=['name', 'month']).agg({'precipitation' : ['count']}).reset_index()
    counts['count'] = counts['precipitation']
    counts = counts.pivot(index='name', columns='month', values='count')
    


    return monthly, counts


data = pd.read_csv('precipitation.csv')

data['month'] = data['date'].map(lambda x: date_to_month(x))
#print(data)

totals, counts = pivot_months_pandas(data)
totals.to_csv('totals.csv')
counts.to_csv('counts.csv')
np.savez('monthdata.npz', totals=totals.values, counts=counts.values)

