import numpy as np
import pandas as pd
import math

def getVector(position1, position2):
    return position2 - position1

def dict2vector2D(value, use_list = False):
    list_ = [value['x'], value['y']]
    if use_list:
        return list_
    else:
        return np.array(list_)

def dict2vector3D(value, use_list = False):
    list_ = [value['x'], value['y'], value['z']]
    if use_list:
        return list_
    else:
        return np.array(list_)



def getAngle(vector1, vector2):

    inner_product = np.inner(vector1, vector2)
    
    norm_v1 = np.linalg.norm(vector1)
    norm_v2 = np.linalg.norm(vector2)

    if norm_v1 == 0.0 or norm_v2 == 0.0:
        return np.nan
    cos = inner_product / (norm_v1*norm_v2)
    # result in radians
    rad = np.arccos(np.clip(cos, -1.0, 1.0))
    # covert to degrees
    theta = np.rad2deg(rad)

    return theta


def getmotionVelocity(data_list, fps=10):

    i = len(data_list) # get dimension of the list
    if i == 1: 
        norm = 0
    elif i == 2:
        a = np.array(data_list[1]) - np.array(data_list[0])
        norm = np.linalg.norm(a) * fps 
    else:
        a = 3/2*np.array(data_list[2]) - 2*np.array(data_list[1]) + 1/2*np.array(data_list[0])
        norm = np.linalg.norm(a) * fps 

    return norm


def getmotionAcceleration(data_list, fps=10):

    i = len(data_list) # get dimension of the list

    if i == 0:
        norm = 0
    elif i == 1:
        a = data_list[1] - data_list[0]
        norm = a * 10 * fps 
    else:
        a = 3/2*data_list[2] - 2*data_list[1] + 1/2*data_list[0]
        norm = a * 10 * fps 

    return norm
 

def getTipDistance(thumb_tip, index_tip, middle_tip ):
 
    t2i = np.array(index_tip) - np.array(thumb_tip) #if index_tip[3] == 1 else 100
    t2m = np.array(middle_tip) - np.array(thumb_tip) #if middle_tip[3] == 1 else 100
    l = min(np.linalg.norm(t2i), np.linalg.norm(t2m))
    return l



    