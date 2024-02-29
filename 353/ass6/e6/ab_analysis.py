import sys
import pandas as pd
import numpy as np
from scipy import stats



OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value:  {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value:  {more_searches_p:.3g} \n'
    '"Did more/less instructors use the search feature?" p-value:  {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value:  {more_instr_searches_p:.3g}'
)


def main():
    searchdata_file = sys.argv[1]

    # ...
    df = pd.read_json(searchdata_file, orient='records', lines=True)
    #print(df)

    new_search = df[df['uid'] % 2 ==1]
    new_search_sum = new_search['search_count'].sum()
    #print(new_search)
    new_counts = new_search['search_count'].value_counts()
    new_sum = new_counts.sum()
    new_count = new_sum - new_counts[0]
    #print("sum", new_sum, "zeros", new_count)
    #print(new_counts)

    old_search = df[df['uid'] % 2 ==0]
    old_search_sum = old_search['search_count'].sum()
    #print(old_search)
    old_counts = old_search['search_count'].value_counts()
    old_sum = old_counts.sum()
    old_count = old_sum + old_counts[0]
    #print("sum", old_sum, "zeros", old_count)
    #print(old_counts)

    all_table1 = np.array([[old_count, new_count], [new_sum, old_sum]])
    all_results1 = stats.chi2_contingency(all_table1)
    
    all_table2 = np.array([[old_search_sum, new_search_sum], [new_sum, old_sum]])
    all_results2 = stats.chi2_contingency(all_table2)

    df = df[df['is_instructor'] == True]

    new_search = df[df['uid'] % 2 ==1]
    new_search_sum = new_search['search_count'].sum()
    #print(new_search)
    new_counts = new_search['search_count'].value_counts()
    new_sum = new_counts.sum()
    new_count = new_sum - new_counts[0]
    #print("sum", new_sum, "zeros", new_count)
    #print(new_counts)

    old_search = df[df['uid'] % 2 ==0]
    old_search_sum = old_search['search_count'].sum()
    #print(old_search)
    old_counts = old_search['search_count'].value_counts()
    old_sum = old_counts.sum()
    old_count = old_sum + old_counts[0]
    #print("sum", old_sum, "zeros", old_count)
    #print(old_counts)

    intructor_table1 = np.array([[old_count, new_count], [new_sum, old_sum]])
    intructor_results1 = stats.chi2_contingency(intructor_table1)

    intructor_table2 = np.array([[old_search_sum, new_search_sum], [new_sum, old_sum]])
    intructor_results2 = stats.chi2_contingency(intructor_table2)

    # Output
    print(OUTPUT_TEMPLATE.format(
        more_users_p=all_results1[1],
        more_searches_p=all_results2[1],
        more_instr_p=intructor_results1[1],
        more_instr_searches_p=intructor_results2[1],
    ))

if __name__ == '__main__':
    main()