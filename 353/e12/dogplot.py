import seaborn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from datetime import datetime
from scipy import stats

def find_rating(x):
    m = re.search(r'(\d+(\.\d+)?)/10', x)
    # print(type(m))
    if isinstance(m, re.Match):
        m = m.group(0).rstrip('/10')
    return m

tweets = pd.read_csv('dog_rates_tweets.csv', parse_dates=['created_at'])
tweets['ratings'] = tweets['text'].apply(lambda x :find_rating(x))
tweets = tweets[(tweets['ratings'].notna())]
tweets = tweets[(tweets['ratings'] != '')]
tweets['ratings'] = tweets['ratings'].apply(lambda x :float(x))
tweets = tweets[(tweets['ratings'] <= 25)]
tweets['timestamp'] = tweets['created_at'].apply(lambda x: x.timestamp())
fit = stats.linregress(tweets['timestamp'].values, tweets['ratings'].values)
tweets['predictions'] = tweets['timestamp'].apply(lambda x: x*fit.slope + fit.intercept)
# print(tweets)

seaborn.set()

plt.plot(tweets['created_at'].values, tweets['ratings'].values, 'b.', alpha= 0.5)
plt.plot(tweets['created_at'].values, tweets['predictions'].values, 'r-', linewidth=3)
# plt.xticks(rotation=25)
plt.xlabel('Year')
plt.ylabel('Rating (x/10)')
plt.savefig('dogpots.png')
# plt.show()

print('Slope:',fit.slope)
print('Intercept:',fit.intercept)
print('Pvalue:', fit.pvalue)


# tweets = tweets.sort_values(by=['timestamp'])
# before_2017 = tweets[(tweets['created_at']<= '2017-01-01 00:00:01')]
# after_2017 = tweets[(tweets['created_at'] > '2017-01-01 00:00:01')]

# above_10_pre_2017 = before_2017[(before_2017['ratings'] > 10)]
# below_10_pre_2017 = before_2017[(before_2017['ratings'] <= 10)]
# percent_above_10_pre_2017 = above_10_pre_2017['ratings'].count() / (above_10_pre_2017['ratings'].count() + below_10_pre_2017['ratings'].count())
# print('Percert above 10 before 2017', percent_above_10_pre_2017)

# above_10_after_2017 = after_2017[(after_2017['ratings'] > 10)]
# below_10_after_2017 = after_2017[(after_2017['ratings'] <= 10)]
# percent_above_10_after_2017 = above_10_after_2017['ratings'].count() / (above_10_after_2017['ratings'].count() + below_10_after_2017['ratings'].count())
# print('Percert above 10 after 2017', percent_above_10_after_2017)

plt.figure(figsize=(10, 6))
residuals = tweets['ratings'] - tweets['predictions']
plt.plot(tweets['created_at'], residuals, marker='o', linestyle='None')
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Date')
plt.ylabel('Residuals')
plt.title('Residual Plot')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# residuals = tweets['ratings'].values - (fit.slope*tweets['timestamp'].values + fit.intercept)
# counts, bins = np.histogram(residuals)
# plt.stairs(counts, bins)
# plt.show()