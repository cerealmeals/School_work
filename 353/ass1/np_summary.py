import numpy as np

data = np.load('353\\ass1\\e1\\monthdata.npz')
totals = data['totals']
counts = data['counts']

# Question 1
print('Row with lowest total precipitation:')
sum = np.sum(totals, axis=1)
lowest = np.argmin(sum)
print(lowest)
#print(np.argmin(np.sum(totals, axis=1)))

# Question 2
print('Average precipitation in each month:')
rain_sum = np.sum(totals, axis=0)
days_sum = np.sum(counts, axis=0)
average = np.divide(rain_sum, days_sum)
print(average)
#print(np.divide(np.sum(totals, axis=0), np.sum(counts, axis=0)))

# Question 3
print('Average precipitation in each city:')
rain_sum = np.sum(totals, axis=1)
days_sum = np.sum(counts, axis=1)
average = np.divide(rain_sum, days_sum)
print(average)
#print(np.divide(np.sum(totals, axis=1), np.sum(counts, axis=1)))

#Question 4
print('Quarterly precipitation totals:')
rows = len(totals)
reshaped = np.reshape(totals, (4*rows, 3))
sum = np.sum(reshaped, axis=1)
shaped= np.reshape(sum, (rows , 4))
print(shaped)
#print(np.reshape(np.sum(np.reshape(totals, (4*len(totals), 3)), axis=1), (len(totals), 4)))