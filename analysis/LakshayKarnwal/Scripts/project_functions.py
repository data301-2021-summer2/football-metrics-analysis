import pandas as pd
from multipledispatch import dispatch
import matplotlib.pyplot as plt


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
    .drop(columns=['xGA_diff','npxG','npxGD','npxGA','wins','draws','loses','xpts_diff','xG_diff','deep','deep_allowed']
    )
    .rename(columns={'Unnamed: 0' :'league','Unnamed: 1':'year','missed':'conceded','ppda_coef':'pressure','oppda_coef':'oppo_pressure'}
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

def weighted_avg(league,year,path):
    
    df= filter_data_set(league,year,path)

    avg= ((df['pressure'])*0.24 + (df['xG'])*0.37 + (df['scored'])*0.39)
    team= df['team']
    position= df['position']
    
    data = list(zip(team, position, avg))
    df1= pd.DataFrame(data,columns=['team','position','avg'])
    df2=df1.style.set_table_attributes("style='display:inline'").set_caption('Weighted avg. of team'+'s effect on opponent')
    fig, ax = plt.subplots()
    bar_plot(ax, df1, total_width=0.3, single_width=0.7, chart_value=3)
    
    display(df2)
    plt.show()
    
    avg=((df['oppo_pressure'])*0.28 + (df['xGA'])*0.34 + (df['conceded'])*0.38)
    data=list(zip(team, position, avg))
    df3=pd.DataFrame(data,columns=['team','position','avg'])
    df4=df3.style.set_caption('Weighted avg. of opponent'+'s effect on team')
    fig, ax = plt.subplots()
    bar_plot(ax, df3, total_width=0.3, single_width=0.7, chart_value=3)
    
    display(df4)
    plt.show()
    
    net=df1['avg']-df3['avg']
    data=list(zip(team, position, net))
    df3=pd.DataFrame(data,columns=['team','position','net'])
    df4=df3.style.set_table_attributes("style='display:inline'").set_caption('Net effect of each team')
    fig, ax = plt.subplots()
    bar_plot(ax, df3, total_width=0.3, single_width=0.7, chart_value=3)
    
    display(df4)
    plt.show()
    

def team_effect_parameters(df):
    df=df.drop(columns=['pts','year','matches','pts_per_game','league','conceded','oppo_pressure','xpts','xGA'])
    return df

def opponent_effect_parameters(df):
    df= df.drop(columns=['pts','year','matches','pts_per_game','league','xG','xpts','scored','pressure'])
    return df


@dispatch(str,int,int, str)
def filter_data_set(league, year, chart_value, path):
    
    df= load_and_process(path)
    
    df1=df[df['year']==year]
    df2=df1[df1['league']==league]
    df3=df2[df2['position']==1]

    xG=[]

    a= (float)(df3['xG'])
    xG.append(a)
    for i in range(0,19):
        xG.append(a)

    df4=df2[df2['xG'].values >= xG]
        
    return df4

@dispatch(str,int, str)
def filter_data_set(league, year, path):
    
    df= load_and_process(path)
    
    df1=df[df['year']==year]
    df2=df1[df1['league']==league]
    df3=df2[df2['position']==1]

    xG=[]

    a= (float)(df3['xG'])
    xG.append(a)
    for i in range(0,19):
        xG.append(a)

    df4=df2[df2['xG'].values >= xG]
    display(df4)
        
    return df4

def bar_plot(ax, data, colors=None, total_width=0.8, single_width=1, legend=True, chart_value=None):
    
    list=[]
    x_pos= data['team']
    for i in range(0,len(data['position'])):
        list.append(i)
    s= pd.Series(list)
    
    if chart_value == 1:
        data= team_effect_parameters(data)
        plt.title('Team\'s effect on opponent (xG, scored, pressure)')
    elif chart_value == 2:
        data= opponent_effect_parameters(data)
        plt.title('Opponent\'s effect on team (xGA, conceded, oppo_pressure)')
    else:
        data=data
        
    data= data.drop(columns=['team','position'])
    
    # Check if colors where provided, otherwhise use the default color cycle
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Number of bars per group
    n_bars = len(data)

    # The width of a single bar
    bar_width = total_width / n_bars

    # List containing handles for the drawn bars, used for the legend
    bars = []

    # Iterate over all data
    for i, (name, values) in enumerate(data.items()):
        # The offset in x direction of that bar
        x_offset = (i - n_bars / 2) * bar_width + bar_width / 2

        # Draw a bar for every value of that type
        for x, y in enumerate(values):
            bar = ax.bar(x + x_offset, y, width=bar_width * single_width, color=colors[i % len(colors)])

        # Add a handle to the last drawn bar, which we'll need for the legend
        bars.append(bar[0])

    # Draw legend if we need
    if legend:
        ax.legend(bars, data.keys())
    
    plt.xticks(s,x_pos)

    plt.xlabel('Teams')
    plt.ylabel('Values')


@dispatch(str,int, str)
def data_filter(league,year, path):
    df1 = load_and_process(path)
    df2 = (
        df1[df1["league"]==league]
        )
    df3 = df2[df2["year"]==year]
    
    return df3

@dispatch(str,str)
def data_filter(league, path):
    df1 = load_and_process(path)
    df2 = (
        df1[df1["league"]==league]
        )
    
    return df2

@dispatch(int,str)
def data_filter(pos, path):
    df1 = load_and_process(path)
    df2 = df1[df1['position']==pos]
    
    return df2
