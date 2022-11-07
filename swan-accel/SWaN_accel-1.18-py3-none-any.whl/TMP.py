import pandas as pd
import datetime, os, sys, glob
import numpy as np


def contigous_regions(condition):
    d = np.diff(condition)
    idx, = d.nonzero()
    idx += 1
    idx = np.r_[0, idx - 1]
    idx = np.r_[idx, condition.size - 1]

    bout_lis = []
    for i in range(len(idx) - 1):
        if i == 0:
            first = idx[i]
        else:
            first = idx[i] + 1
        second = idx[i + 1]
        bout_lis = bout_lis + [[first, second]]

    this_ar = np.asarray(bout_lis)

    return this_ar


s_fi = "C:/Users\BINOD\Desktop\DS_15_Night1_sleep_label.csv"
this_sleep_df = pd.read_csv(s_fi, parse_dates=['START_TIME','STOP_TIME'], compression='infer')
this_sleep_df.replace({'Wake': 0, 'N1': 1, 'N2': 1, 'N3':1, 'REM':1}, inplace=True)
this_sleep_df['REFERENCE_PREDICTION'] = this_sleep_df['PREDICTION'].shift(1)
this_sleep_df['DIFF'] = this_sleep_df['PREDICTION'] - this_sleep_df['REFERENCE_PREDICTION']
start_index_lis = this_sleep_df[this_sleep_df['DIFF'] == 1].index.values
start_index = start_index_lis[0]
stop_index_lis = this_sleep_df[this_sleep_df['DIFF'] == -1].index.values
stop_index = stop_index_lis[-1]-1

new_sleep_df = this_sleep_df.loc[start_index:stop_index,:]

cond = new_sleep_df['PREDICTION'].values

bout_array = contigous_regions(cond)
bout_df = pd.DataFrame(bout_array, columns=['START_IND', 'STOP_IND'])

for bout_ind, bout_row in bout_df.iterrows():
    start, end = bout_row['START_IND'] + start_index, bout_row['STOP_IND']+start_index

    if(start!=end):
        print(this_sleep_df.loc[start,'START_TIME'],this_sleep_df.loc[end,'STOP_TIME'])




# new_sleep_df.to_csv("C:/Users\BINOD\Desktop\DS_15_Night1_sleep_label_onlysleep.csv",index=False,float_format='%.1f')