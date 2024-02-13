import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from datetime import date
from scipy import stats

OUTPUT_TEMPLATE = (
    "Initial T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann-Whitney U-test p-value: {utest_p:.3g}"
)

def is_weekend(x):
    x = date.weekday(x)
    if(x >4):
        return 1
    return 0

def main():
    df = pd.read_json(sys.argv[1], lines=True)
    
    #print(type(df['date'].values[0]))
    df = df[df['subreddit'] == 'canada']
    df = df[ (df['date'] < np.datetime64('2014-01-01')) & (df['date']> np.datetime64('2011-12-31'))]
    df['weekend'] = df['date'].apply(lambda x: is_weekend(x))
    weekdays = df[df['weekend'] == 0]
    weekends = df[df['weekend'] == 1]
    #plt.plot(df['comment_count'].values, df['weekend'].values, 'b.', alpha=0.5)
    #plt.savefig('data.png')
    
    s = stats.ttest_ind(weekdays['comment_count'].values, weekends['comment_count'].values)
    

    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p=s.pvalue,
        initial_weekday_normality_p=0,
        initial_weekend_normality_p=0,
        initial_levene_p=0,
        transformed_weekday_normality_p=0,
        transformed_weekend_normality_p=0,
        transformed_levene_p=0,
        weekly_weekday_normality_p=0,
        weekly_weekend_normality_p=0,
        weekly_levene_p=0,
        weekly_ttest_p=0,
        utest_p=0,
    ))


if __name__ == '__main__':
    main()