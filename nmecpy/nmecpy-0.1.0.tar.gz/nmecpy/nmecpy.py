# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 09:59:57 2022

@author: dluu
"""

from helpers import *
from sklearn.linear_model import LinearRegression
import pandas as pd

def model_with_TOWT(df, time_interval, knot_temps=[40, 55, 65, 80, 90]):
    # df: pandas dataframe consisting of energy usage, timestamp, and temperature
    # time_interval: string noting whether analysis is "Daily" or "Hourly"
    # knot_temps: list containing the knot temperatures. Defaulted if empty.
    
    # Define knot temp vars and tow vars from helper functions
    temp_vars, used_knot_temps = towt_temp_vars(df, knot_temps)
    tow_vars = define_tow_vars(df, time_interval)
    
    # assemble regression datasets
    if 'occ' not in df.columns:
        df['occ'] = 1
        
    main = pd.concat([df, temp_vars, tow_vars], axis = 1)
    train = main.dropna().copy()
    train.drop(columns = ['time', 'temp'], inplace = True)
    
    ## Create models and predict
    # Occupied model
    occ_y_train = train.loc[train['occ']==1, 'load']
    occ_x_train = train.loc[train['occ']==1, train.columns != 'load']
    occ_x_train.drop(columns = 'occ', inplace = True)
    occ_model = LinearRegression().fit(occ_x_train, occ_y_train)
    occ_x_train['predict'] = occ_model.predict(occ_x_train)
    
    # Unoccupied model
    unocc_model = None
    if train['occ'].nunique() > 1:
        unocc_y_train = train.loc[train['occ']==0, 'load']
        unocc_x_train = train.loc[train['occ']==0, train.columns != 'load']
        unocc_x_train.drop(columns = 'occ', inplace = True)
        unocc_model = LinearRegression().fit(unocc_x_train, unocc_y_train)
        unocc_x_train['predict'] = unocc_model.predict(unocc_x_train)
        
    # Merge dataset back together
    occ_train = pd.concat([occ_x_train, occ_y_train], axis = 1)
    unocc_train = pd.concat([unocc_x_train, unocc_y_train], axis = 1)
    train_estimate = pd.concat([occ_train, unocc_train])
    train_estimate = pd.concat([main, train_estimate['predict']], axis = 1)
    
    output = {"occupied model": occ_model,
              "unoccupied model": unocc_model,
              "data": train_estimate}
    
    return(output)