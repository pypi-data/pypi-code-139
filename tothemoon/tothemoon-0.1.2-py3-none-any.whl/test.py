import pandas as pd
from moon import signal, Regbot
from tothemoon.moon import signal as sig

df = pd.read_csv('/home/defi/Desktop/portfolio/projects/python/jupyter/tothemoon_validation_v011.csv')
def getSignal(open,close,utcdatetime):
    return signal(open,close,utcdatetime)

# select long profitable trades
df2 = df[df['close_profit_abs'] < 0]
df2 = df2[df2['is_short'] == 0]
print(df2.head())

# Run all predictions
df2['enter_long_pred'] = df.apply(lambda row: getSignal(row['open'], row['close'], row['date']), axis=1)

print(len(df2[df2['enter_long_pred'] == df2['is_short']]), len(df) )

print(df2[df2['is_short']==0].head(15))