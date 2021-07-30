import pandas as pd
from multipledispatch import dispatch
import matplotlib.pyplot as plt

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
    .drop(columns=['xGA_diff','npxG','npxGD','deep','deep_allowed','npxGA','wins','draws','loses']
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

def bar_plot(ax, data, colors=None, total_width=0.8, single_width=1, legend=True):
    """Draws a bar plot with multiple bars per data point.

    Parameters
    ----------
    ax : matplotlib.pyplot.axis
        The axis we want to draw our plot on.

    data: dictionary
        A dictionary containing the data we want to plot. Keys are the names of the
        data, the items is a list of the values.

        Example:
        data = {
            "x":[1,2,3],
            "y":[1,2,3],
            "z":[1,2,3],
        }

    colors : array-like, optional
        A list of colors which are used for the bars. If None, the colors
        will be the standard matplotlib color cyle. (default: None)

    total_width : float, optional, default: 0.8
        The width of a bar group. 0.8 means that 80% of the x-axis is covered
        by bars and 20% will be spaces between the bars.

    single_width: float, optional, default: 1
        The relative width of a single bar within a group. 1 means the bars
        will touch eachother within a group, values less than 1 will make
        these bars thinner.

    legend: bool, optional, default: True
        If this is set to true, a legend will be added to the axis.
    """

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