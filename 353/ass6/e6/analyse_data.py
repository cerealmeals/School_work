import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from scipy import stats


def main():
    df = pd.read_csv(sys.argv[1])

    qs1 = df[df['type'] == 'qs1']
    qs2 = df[df['type'] == 'qs2']
    qs3 = df[df['type'] == 'qs3']
    qs4 = df[df['type'] == 'qs4']
    qs5 = df[df['type'] == 'qs5']
    merge1 = df[df['type'] == 'merge1']
    partition_sort = df[df['type'] == 'partition_sort']
    
    ttest = [['qs1 vs qs2', stats.ttest_ind(qs1['time'], qs2['time']).pvalue]]
    ttest.append(['qs1 vs qs3', stats.ttest_ind(qs1['time'], qs3['time']).pvalue])
    ttest.append(['qs1 vs qs4', stats.ttest_ind(qs1['time'], qs4['time']).pvalue])
    ttest.append(['qs1 vs qs5', stats.ttest_ind(qs1['time'], qs5['time']).pvalue])
    ttest.append(['qs2 vs qs3', stats.ttest_ind(qs2['time'], qs3['time']).pvalue])
    ttest.append(['qs2 vs qs4', stats.ttest_ind(qs2['time'], qs4['time']).pvalue])
    ttest.append(['qs2 vs qs5', stats.ttest_ind(qs2['time'], qs5['time']).pvalue])
    ttest.append(['qs3 vs qs4', stats.ttest_ind(qs3['time'], qs4['time']).pvalue])
    ttest.append(['qs3 vs qs5', stats.ttest_ind(qs3['time'], qs5['time']).pvalue])
    ttest.append(['qs4 vs qs5', stats.ttest_ind(qs4['time'], qs5['time']).pvalue])
    ttest.append(['qs1 vs merge1', stats.ttest_ind(qs1['time'], merge1['time']).pvalue])
    ttest.append(['qs1 vs partition_sort', stats.ttest_ind(qs1['time'], partition_sort['time']).pvalue])
    ttest.append(['qs2 vs merge1', stats.ttest_ind(qs2['time'], merge1['time']).pvalue])
    ttest.append(['qs2 vs partition_sort', stats.ttest_ind(qs2['time'], partition_sort['time']).pvalue])
    ttest.append(['qs3 vs merge1', stats.ttest_ind(qs3['time'], merge1['time']).pvalue])
    ttest.append(['qs3 vs partition_sort', stats.ttest_ind(qs3['time'], partition_sort['time']).pvalue])
    ttest.append(['qs4 vs merge1', stats.ttest_ind(qs4['time'], merge1['time']).pvalue])
    ttest.append(['qs4 vs partition_sort', stats.ttest_ind(qs4['time'], partition_sort['time']).pvalue])
    ttest.append(['qs5 vs merge1', stats.ttest_ind(qs5['time'], merge1['time']).pvalue])
    ttest.append(['qs5 vs partition_sort', stats.ttest_ind(qs5['time'], partition_sort['time']).pvalue])
    ttest.append(['merge1 vs partition_sort', stats.ttest_ind(merge1['time'], partition_sort['time']).pvalue])

    means = [['qs1', qs1['time'].mean()]]
    means.append(['qs2', qs2['time'].mean()])
    means.append(['qs3', qs3['time'].mean()])
    means.append(['qs4', qs4['time'].mean()])
    means.append(['qs5', qs5['time'].mean()])
    means.append(['merge1', merge1['time'].mean()])
    means.append(['partition_sort', partition_sort['time'].mean()])

    df1 = pd.DataFrame(ttest, columns=['comparing', 'Pvalue'])
    df2 = pd.DataFrame(means, columns=['name', 'value'])
    df2 = df2.sort_values(by=['value'])
    print(df2)
    print(df1)


if __name__ == '__main__':
    main()