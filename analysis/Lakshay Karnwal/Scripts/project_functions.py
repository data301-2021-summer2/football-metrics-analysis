import pandas as pd
from multipledispatch import dispatch

def printing():
    print("Hello world")

def load_and_process(path):

    # Method Chain 1 (Load data and deal with missing data)

    df1 = (
        pd.read_csv(path
        )
        .dropna(axis=0 #new line added
        )
        #.shape(
        
    )

    # Method Chain 2 (Create new columns, drop others, and do processing)

    df2 = (
          df1
    .assign(pts_per_game = lambda df: df['pts']/df['matches']
    )
    .drop(columns=['xGA_diff','npxG','npxGD','ppda_coef','deep','deep_allowed','npxGA','oppda_coef','wins','draws','loses']
    )
    .rename(columns={'Unnamed: 0' :'league','Unnamed: 1':'year','missed':'conceded'}
    )
    .set_index('league'
    )
    .drop('RFPL'
    )
    .reset_index(
    )
     )

    # Make sure to return the latest dataframe

    return df2

def filter_data_set(league, year):
    
    df= load_and_process("../../data/raw/understat.com.csv")
    
    df1=df[df['year']==year]
    df2=df1[df1['league']==league]
    df3=df2[df2['position']==1]

    xG=[]

    a= (float)(df3['xG'])
    xG.append(a)
    for i in range(0,19):
        xG.append(a)
    #print(xG)

    df4=df2[df2['xG'].values >= xG]
    #print(df2['xG'])
    
    return df4

@dispatch(str,int)
def data_filter(league,year):
    df1 = load_and_process("../../data/raw/understat.com.csv")
    df2 = (
        df1[df1["league"]==league]
        )
    df3 = df2[df2["year"]==year]
    
    return df3

@dispatch(str)
def data_filter(league):
    df1 = load_and_process("../../data/raw/understat.com.csv")
    df2 = (
        df1[df1["league"]==league]
        )
    
    return df2

@dispatch(int,str)
def data_filter(pos, path):
    df1 = load_and_process(path)
    df2 = df1[df1['position']==pos]
    
    return df2

#load_and_process("../../data/raw/understat.com.csv")
#league_filter("EPL",2014)