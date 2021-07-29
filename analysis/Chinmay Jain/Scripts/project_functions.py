import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from multipledispatch import dispatch 

def load_and_process(path):

    # Method Chain 1 (Load data and deal with missing data)

    df1 = (
        pd.DataFrame(
            pd.read_csv(path)
        )
        .dropna(axis=0)
        #.shape()
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

def weighted_av(path):
    df_av = pd.DataFrame(data_filter("La_liga", path), index=[0])
    df_av = df_av.append(data_filter("EPL", path), ignore_index=True)
    df_av = df_av.append(data_filter("Bundesliga", path), ignore_index=True)
    df_av = df_av.append(data_filter("Serie_A", path), ignore_index=True)
    df_av = df_av.append(data_filter("Ligue_1", path), ignore_index=True)
    
    df_av['Offensive W_Average'] = 0.5*df_av['xG'] + 0.25*df_av['ppda_coef'] + 0.25*df_av['deep']
    df_av['Defensive W_Average'] = 0.45*df_av['xGA'] + 0.35*df_av['oppda_coef'] + 0.2*df_av['deep_allowed']
    df_av = df_av.drop(columns = ['pts', 'xG', 'xGA', 'ppda_coef', 'oppda_coef', 'deep', 'deep_allowed'])
    
    df_top = pd.DataFrame(data_filter("La_liga",1, path), index=[0])
    df_top = df_top.append(data_filter("EPL",1, path), ignore_index=True)
    df_top = df_top.append(data_filter("Bundesliga",1, path), ignore_index=True)
    df_top = df_top.append(data_filter("Serie_A",1, path), ignore_index=True)
    df_top = df_top.append(data_filter("Ligue_1",1, path), ignore_index=True)
    
    df_top['Offensive W_Average'] = 0.5*df_top['xG'] + 0.25*df_top['ppda_coef'] + 0.25*df_top['deep']
    df_top['Defensive W_Average'] = 0.45*df_top['xGA'] + 0.35*df_top['oppda_coef'] + 0.2*df_top['deep_allowed']
    df_top = df_top.drop(columns = ['pts', 'xG', 'xGA', 'ppda_coef', 'oppda_coef', 'deep', 'deep_allowed'])
    #df_top = df_top.rename(columns={'League':'Top Team'})
    df=pd.concat([df_top,df_av])
    df = df.sort_values(by=['League'], ignore_index=True)
    #df = pd.merge(df_av, df_top, how = 'outer')
    return df
    
    


    