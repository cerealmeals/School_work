import sys
import pandas as pd
import numpy as np
import difflib 

def sort_ratings(x, df, lst):
    matche = difflib.get_close_matches(x['title'], lst, n=1)
    if matche != []:
        df.loc[matche[0], ['total']] += x['rating']
        df.loc[matche[0], ['count']] += 1
        # df.loc[df['title']==matche[0], ['total']] += x['rating']
        # df.loc[df['title']==matche[0], ['count']] += 1

def main():
    df = pd.DataFrame(columns=['title','rating','count','total'])
    df['title'] = pd.read_csv(sys.argv[1], delimiter="\t")
    df['count'] = df['count'].fillna(0)
    df['total'] = df['total'].fillna(0)
    df = df.set_index('title')
    #print(df)

    mess = pd.read_csv(sys.argv[2])
    #print(mess)
    lst = df.index.to_list()
    #print(lst)
    mess.apply(lambda x: sort_ratings(x, df, lst), axis=1)
    df['rating'] = (df['total']/df['count']).round(2)
    df = df.drop(columns=['count', 'total'])
    #df = df.reset_index()
    #print(df)
    df.to_csv(sys.argv[3], index=True)



if __name__ == '__main__':
    main()