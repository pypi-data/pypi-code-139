#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/7 18:39
# @Author  : 马赫
# @Email   : 1692303843@qq.com
# @FileName: verify.py

from BiVFM.func import *
from BiVFM.olga_func import *
from BiVFM.model import *
from BiVFM.feature_engineering import *
from BiVFM.config_transfer import *
from BiVFM.train_func import *

def valid_metric():
    # 误差指标分析
    print('==================== 性能指标分析 ====================')

    def MAE(y, y_pre):
        return round(np.mean(np.abs(y - y_pre)), 7)

    def MSE(y, y_pre):
        return round(np.mean((y - y_pre) ** 2), 7)

    def RMSE(y, y_pre):
        return round(np.sqrt(MSE(y, y_pre)), 7)

    def MAPE(y, y_pre):
        return round(np.mean(np.abs((y - y_pre) / y)), 7)

    def R2(y, y_pre):
        u = np.sum((y - y_pre) ** 2)
        v = np.sum((y - np.mean(y)) ** 2)
        return round(1 - (u / v), 7)

    def loss_list(y, y_pre):
        print('MAE', MAE(y, y_pre))
        print('MSE', MSE(y, y_pre))
        print('RMSE', RMSE(y, y_pre))
        print('MAPE', MAPE(y, y_pre))
        print('R2', R2(y, y_pre))


    loss_y, loss_y_pred = y_gt[:100, 0], y_predict[:100, 0]
    loss_list(loss_y, loss_y_pred)
    print()
    loss_y, loss_y_pred = y_gt[100: 300, 0], y_predict[100: 300, 0]
    loss_list(loss_y, loss_y_pred)
    print()
    loss_y, loss_y_pred = y_gt[:, 0], y_predict[:, 0]
    loss_list(loss_y, loss_y_pred)



