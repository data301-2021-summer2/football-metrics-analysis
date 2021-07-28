import pandas as pd
import numpy as np
from multipledispatch import dispatch 

def load_and_process(path):

    # Method Chain 1 (Load data and deal with missing data)

    df1 = (
        pd.DataFrame(
            pd.read_csv(path)
        )
    )
    # Method Chain 2 (Create new columns, drop others, and do processing)

    df2 = (
        df1
        .drop(
            columns = ['wins', 'draws', 'loses','scored', 'missed','npxG', 'xG_diff', 'xGA_diff', 'npxGA', 'npxGD', 'xpts', 'xpts_diff']
        )
        .rename(
            columns={'Unnamed: 0': 'League', 'Unnamed: 1':'Year'}
        )
        .set_index(
            'League'
        )
        .drop(
            'RFPL'
        )
        .reset_index()
    )

    # Make sure to return the latest dataframe

    return df2

@dispatch(str, int, str)
def data_filter(league, pos, path):
    df1 = load_and_process(path)
    df2 = (
        df1[df1["League"]==league]
        )
    df3 = df2[df2['position']==pos]
    av = {'League':league+"_topTeam", 'pts': df3['pts'].mean(), 'xG':df3['xG'].mean(), 'xGA':df3['xGA'].mean(), 'ppda_coef':df3['ppda_coef'].mean(), 'oppda_coef':df3['oppda_coef'].mean(), 'deep':df3['deep'].mean(), 'deep_allowed':df3['deep_allowed'].mean()}
    return av

@dispatch(int,str)
def data_filter(pos, path):
    df1 = load_and_process(path)
    df2 = df1[df1['position']==pos]
    
    return df2

@dispatch(str, str)
def data_filter(league,path):
    df1 = load_and_process(path)
    df2 = (
        df1[df1["League"]==league]
        )
    df2 = df2.drop(
        columns = ['Year', 'position', 'team', 'matches']
    )
    av = {'League':league, 'pts': df2['pts'].mean(), 'xG':df2['xG'].mean(), 'xGA':df2['xGA'].mean(), 'ppda_coef':df2['ppda_coef'].mean(), 'oppda_coef':df2['oppda_coef'].mean(), 'deep':df2['deep'].mean(), 'deep_allowed':df2['deep_allowed'].mean()}
    
    return av