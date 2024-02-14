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

def calendar(x):
    x = date.isocalendar(x)
    tup = (x.year, x.week)
    return tup

def main():
    df = pd.read_json(sys.argv[1], lines=True)
    
    #print(type(df['date'].values[0]))
    df = df[df['subreddit'] == 'canada']
    df = df[ (df['date'] < np.datetime64('2014-01-01')) & (df['date']> np.datetime64('2011-12-31'))]
    df['calendar'] = df['date'].apply(lambda x: calendar(x))
    df['weekend'] = df['date'].apply(lambda x: is_weekend(x))
    weekdays = df[df['weekend'] == 0]
    weekends = df[df['weekend'] == 1]
    print('average weekday:', weekdays['comment_count'].agg('mean'))
    print('average weekend:', weekends['comment_count'].agg('mean'))
    #plt.plot(df['comment_count'].values, df['weekend'].values, 'b.', alpha=0.5)
    #plt.savefig('data.png')
    #print(weekdays)
    #print(weekends)
    s = stats.ttest_ind(weekdays['comment_count'].values, weekends['comment_count'].values)
    days_normal = stats.normaltest(weekdays['comment_count'].values)
    ends_normal = stats.normaltest(weekends['comment_count'].values)
    levene = stats.levene(weekdays['comment_count'].values, weekends['comment_count'].values)
    
    Tweekends = np.log(weekends['comment_count'].values)
    Tweekdays = np.log(weekdays['comment_count'].values)
    
    Tdays_normal = stats.normaltest(Tweekdays)
    Tends_normal = stats.normaltest(Tweekends)
    Tlevene = stats.levene(Tweekdays, Tweekends)

    

    daysgrouped = weekdays.groupby(by='calendar').comment_count.agg('mean')
    endsgrouped = weekends.groupby(by='calendar').comment_count.agg('mean')
    
    Cdays_normal = stats.normaltest(daysgrouped)
    Cends_normal = stats.normaltest(endsgrouped)
    Clevene = stats.levene(daysgrouped, endsgrouped)
    C = stats.ttest_ind(daysgrouped, endsgrouped)

    U_test = stats.mannwhitneyu(weekdays['comment_count'].values, weekends['comment_count'].values)

    # counts, bins = np.histogram(endsgrouped)
    # plt.stairs(counts, bins)
    # plt.savefig('test_log_data.png')

    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p=s.pvalue,
        initial_weekday_normality_p=days_normal.pvalue,
        initial_weekend_normality_p=ends_normal.pvalue,
        initial_levene_p=levene.pvalue,
        transformed_weekday_normality_p=Tdays_normal.pvalue,
        transformed_weekend_normality_p=Tends_normal.pvalue,
        transformed_levene_p=Tlevene.pvalue,
        weekly_weekday_normality_p=Cdays_normal.pvalue,
        weekly_weekend_normality_p=Cends_normal.pvalue,
        weekly_levene_p=Clevene.pvalue,
        weekly_ttest_p=C.pvalue,
        utest_p=U_test.pvalue,
    ))


if __name__ == '__main__':
    main()