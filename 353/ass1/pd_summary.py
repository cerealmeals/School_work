import pandas as pd

totals = pd.read_csv('353\\ass1\\e1\\totals.csv').set_index(keys=['name'])
counts = pd.read_csv('353\\ass1\\e1\\counts.csv').set_index(keys=['name'])

print(totals)

# question 1
print('City with lowest total precipitation:')
row_sums = pd.DataFrame.sum(totals, axis=1)
lowest = row_sums.idxmin()
print(lowest)
#print(pd.DataFrame.sum(totals, axis=1).idxmin())

# Question 2
print('Average precipitation in each month:')
rain_sum = pd.DataFrame.sum(totals, axis=0)
days_sum = pd.DataFrame.sum(counts, axis=0)
average = rain_sum.divide(days_sum)
print(average)
#print(pd.DataFrame.sum(totals, axis=0).divide(pd.DataFrame.sum(counts, axis=0)))

# Question 3
print('Average precipitation in each city:')
rain_sum = pd.DataFrame.sum(totals, axis=1)
days_sum = pd.DataFrame.sum(counts, axis=1)
average = rain_sum.divide(days_sum)
print(average)
#print(pd.DataFrame.sum(totals, axis=1).divide(pd.DataFrame.sum(counts, axis=1)))
