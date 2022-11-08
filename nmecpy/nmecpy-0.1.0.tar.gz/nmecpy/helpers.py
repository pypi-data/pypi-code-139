# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 15:06:45 2022

@author: dluu
"""

import pandas as pd

############################## Temp vars for TOWT #############################
def temp0(temp, knot_temp):
    # temp: temperature value from the 'temp' column in the main dataframe
    # knot_temp: The lowest knot temperature
    
    if temp > knot_temp:
        return(knot_temp)
    else:
        return(temp)

def tempi(temp, knot_tempi, knot_tempj):
    # tempi: temperature value from the 'temp' column in the main dataframe
    # knot_tempi: A knot temperature that is not the lowest or greatest
    # knot_tempj: A knot temperature that is one index lower than i
    
    if temp > knot_tempi:
        return(knot_tempi - knot_tempj)
    else:
        if temp > knot_tempj:
            return(temp - knot_tempj)
        else:
            return(0)


def tempn(temp, knot_tempn):
    # temp: temperature value from the 'temp' column in the main dataframe
    # knot_tempn: The highest knot temperature
    # knot_tempj: A knot temperature that is one index lower than the highest knot temperature
    
    if temp > knot_tempn:
        return(temp - knot_tempn)
    else:
        return(0)
        
    
def towt_temp_vars(df, knot_temps):
    # df: pandas dataframe consisting of at a minimum temperature data labelled "temp".
    # knot_temps: list of knot temperature values
    # Outputs a dataframe with the knot_temp_vars and a list of final the knot_temps used
    
    # Define min and max temperatures in dataset
    min_temp = df['temp'].min()
    max_temp = df['temp'].max()
    
    # Drop outside knot temperature bounds if redundant
    knot_temps = [x for x in knot_temps if x > min_temp]
    knot_temps = [x for x in knot_temps if x < max_temp]
    
    # Sort knot temperatures from least to greatest
    knot_temps.sort()
    
    # Create the temperature variables according to LBNL algo (Mathieu)
    temp_var_dict = {}
    for i in range(len(knot_temps)):
        idx = 'temp'+str(i)
        if i==0:
            temp_var_dict[idx] = df['temp'].apply(temp0, args=(knot_temps[i],)).values
        elif i==len(knot_temps)-1:
            temp_var_dict[idx] = df['temp'].apply(tempi, args = (knot_temps[i], knot_temps[i-1])).values
            temp_var_dict['temp'+str(i+1)] = df['temp'].apply(tempn, args=(knot_temps[i],)).values
        else:
            temp_var_dict[idx] = df['temp'].apply(tempi, args = (knot_temps[i], knot_temps[i-1])).values
    
    return pd.DataFrame(temp_var_dict), knot_temps

###############################################################################

############################## TOW vars for TOWT ##############################
def define_tow_vars(df, time_interval):
    # df: pandas dataframe consisting of at a minimum a timestamp column labelled "time"
    # time_interval: a string noting the data interval (Daily or Hourly)
    
    if time_interval.upper()=='DAILY':
        dow = df['time'].dt.day_name()
        tow_vars = pd.get_dummies(dow)
        return(tow_vars)
    
    elif time_interval.upper()=='HOURLY':
        dow = df['time'].dt.dayofweek
        hour = df['time'].dt.hour
        tow = dow*24 + hour
        tow_vars = pd.get_dummies(tow, prefix = "hour")
        return(tow_vars)
    
###############################################################################

'''
############################# Validate data types #############################
def infer_date_col(df):
    # df: pandas dataframe consisting of a date column
    
    # Finds columns that have a datetime64 data type
    dt64cols = df.columns[df.dtypes.apply(lambda x: pd.api.types.is_datetime64_any_dtype(x))]
    
    # Finds if dataframe has any columns with common date/time column names
    '''