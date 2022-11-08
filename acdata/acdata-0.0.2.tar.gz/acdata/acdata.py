import numpy as np
import pandas as pd
import math
import plotly.express as px
import seaborn as sns
from matplotlib import pyplot as plt
def acdata(data, class_column, samples):
    t = np.linspace(-np.pi, np.pi, samples)
    vals = data.drop(class_column, axis=1).values.T

    curves = np.outer(vals[0], np.ones_like(t))
    for i in range(1, len(vals)):
        ft = ((i + 1) // 2) * t
        if i % 2 == 1:
            curves += np.outer(vals[i], np.sin(ft))
        else:
            curves += np.outer(vals[i], np.cos(ft))
    df = pd.DataFrame({'t': np.tile(np.arange(samples), curves.shape[0]),
                       'sample': np.repeat(np.arange(curves.shape[0]), curves.shape[1]),
                       'f(t)': curves.ravel(),
                       class_column: np.repeat(data[class_column], samples)})
    for cols in data.drop(class_column, axis=1).columns.unique():
        df[cols] = np.repeat(data[cols], samples)
    df['t'] = (((df['t'] - df['t'].min()) /(df['t'].max()-df['t'].min())) - 0.5) * (math.pi *2)
    return df
def plotly_andrews_curves(data, class_column, samples):
    df = acdata(data, class_column, samples)
    fig = px.scatter(df, x = 't', y = 'f(t)', color = class_column)
    return fig
def seaborn_andrews_curves(data, class_column, samples):
    df = acdata(data, class_column, samples)
    sns.set_theme(style = "darkgrid")
    plt.figure(figsize=(15,8))
    fig = sns.lineplot(x = 't', y = 'f(t)', hue = class_column,
                       data = df)
    return fig


    
    