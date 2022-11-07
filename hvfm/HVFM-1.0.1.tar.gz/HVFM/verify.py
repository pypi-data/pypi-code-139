#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/7 18:39
# @Author  : 马赫
# @Email   : 1692303843@qq.com
# @FileName: verify.py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from BiVFM.func import *
from BiVFM.olga_func import *
from BiVFM.model import *
from BiVFM.feature_engineering import *
from BiVFM.config_transfer import *
from BiVFM.train_func import *

# %% BASE LOAD
base_yaml_path = 'olga_work1/conf_1_MFTcNeXt_epoch300.yaml'

base_conf = get_base_config(base_yaml_path)
# print(base_conf)

pkl_dir = base_conf['pkl_dir']
num_epoch = base_conf['num_epoch']
input_channels = base_conf['input_channels']
output_channels = base_conf['output_channels']

continue_epoch = base_conf['continue_epoch']  # 从多少轮开始训练

ratio = base_conf['ratio']
model_name = base_conf['model_name']

load_model = base_conf['load_model']

# 加载数据
raw_data_list = pickle_load('%s/raw_data_list.pkl' % pkl_dir)
print('Number of sample files:', len(raw_data_list))

# 以全部文件作为标准化基准
all_mean = []
all_std = []
for i in raw_data_list:
    mean = i.mean()
    std = i.std()
    all_mean.append(mean)
    all_std.append(std)

all_mean = pd.concat(all_mean, axis=1).T
all_std = pd.concat(all_std, axis=1).T

standardized_args = (all_mean.mean(), all_std.mean())

stand_data_list = [raw2stand(raw_data, standardized_args) for raw_data in raw_data_list]

feature_list = np.array(raw_data_list[0].columns)

x_feature = list(range(len(feature_list)))[:-output_channels]
y_feature = list(range(len(feature_list)))[-output_channels:]

print('x特征%s列，y特征%s列' % (len(x_feature), len(y_feature)))
print('========== x_feature: ==========\n%s' % feature_list[x_feature])
print('========== y_feature: ==========\n%s' % feature_list[y_feature])

np.random.seed(0)
np.random.shuffle(stand_data_list)

num_ratio = int(len(stand_data_list) * ratio)
train_data_list = stand_data_list[: num_ratio]
test_data_list = stand_data_list[num_ratio:]

# DataLoader
train_reader = MyIterableDataset(train_data_list, base_conf['x_length'], base_conf['y_length'], x_feature,
                                 y_feature)

test_reader = MyIterableDataset(test_data_list[: 10], base_conf['x_length'], base_conf['y_length'],
                                x_feature,
                                y_feature, return_y_info=False)

train_loader = DataLoader(train_reader, batch_size=base_conf['batch_size'], drop_last=False)
test_loader = DataLoader(test_reader, batch_size=base_conf['batch_size'], drop_last=False)

for batch_id, (data, label) in enumerate(train_loader()):
    print('train batch x, y_gt shape\t', data.shape, label.shape)
    break

# scalar_s2r = None
# scalar_s2r_x = (standardized_args[0].iloc[x_feature].values, standardized_args[1].iloc[x_feature].values)
scalar_s2r_y = (standardized_args[0].iloc[y_feature].values, standardized_args[1].iloc[y_feature].values)

# %% model list verify

verify_ans = {'model_name': [], 'y_predict': [], 'y_gt': []}

base_yaml_path_list = [
    'olga_work1/conf_1_LSTM_epoch300.yaml',
    'olga_work1/conf_1_Transformer_epoch300.yaml',
    'olga_work1/conf_1_TCN_epoch300.yaml',
    'olga_work1/conf_1_MFTcNeXt_epoch300.yaml',
]
for base_yaml_path in base_yaml_path_list:
    base_conf = get_base_config(base_yaml_path)
    # print(base_conf)

    pkl_dir = base_conf['pkl_dir']
    num_epoch = base_conf['num_epoch']
    input_channels = base_conf['input_channels']
    output_channels = base_conf['output_channels']

    continue_epoch = base_conf['continue_epoch']  # 从多少轮开始训练

    ratio = base_conf['ratio']
    model_name = base_conf['model_name']

    load_model = base_conf['load_model']


    a = Net(input_channels, output_channels, time_steps=base_conf['y_length'], model=model_name)

    shape = (128, base_conf['y_length'], input_channels)

    print('======= Model:%s, input shape %s, output shape %s =======' % (model_name, shape, a(paddle.randn(shape)).shape))
    # print(paddle.summary(a, shape))
    total_params = paddle.summary(a, shape)['total_params']

    net = Net(input_channels, output_channels, time_steps=base_conf['y_length'], model=model_name)
    opt = Adam(learning_rate=2e-4, parameters=net.parameters())  # Adam
    loss_fc = LossFC()

    if load_model:
        try:
            load_params(net, model_path=base_conf['model_path'], opt=opt, opt_path=base_conf['opt_path'])
            log('模型已加载', log_file=base_conf['other_log_file'])
        except Exception as e:
            log('未加载模型', log_file=base_conf['other_log_file'])

    else:
        log('未加载模型', log_file=base_conf['other_log_file'])


    valid_img_save_path = '%s/log_valid/%s.jpg' % (base_conf['base_dir'], model_name)

    y_predict, y_gt = visualization(model=net, loader=test_loader,
                                    standardized_args=scalar_s2r_y,
                                    is_show=True, save_path=valid_img_save_path,
                                    title=feature_list[y_feature],
                                    show_error=False)

    verify_ans['model_name'].append(model_name)

    verify_ans['y_predict'].append(y_predict)
    verify_ans['y_gt'].append(y_gt)


# %%

def MSE(actual, predict):
    return np.mean((actual - predict) ** 2, axis=0)

def RMSE(actual, predict):
    return np.sqrt(MSE(actual, predict))


def MAE(actual, predict):
    return np.mean(np.abs(actual - predict), axis=0)

def MAPE(actual, predict):
    return np.mean(np.abs((actual - predict) / actual), axis=0)

def MAPE_percentage(actual, predict):
    return np.abs((actual - predict) / actual)


def R2(actual, predict):
    u = np.sum((actual - predict) ** 2, axis=0)
    v = np.sum((actual - np.mean(actual, axis=0)) ** 2, axis=0)
    return 1 - (u / v)


all_metric_df = []
for num, model_name in enumerate(verify_ans['model_name']):
    y_gt, y_predict = verify_ans['y_gt'][num], verify_ans['y_predict'][num]
    rmse = RMSE(y_gt, y_predict)
    mae = MAE(y_gt, y_predict)
    mape = MAPE(y_gt, y_predict)

    metric_df = pd.DataFrame({'rmse': rmse, 'mae': mae, 'mape': mape, }).T
    metric_df.columns = [i+'_'+model_name for i in feature_list[y_feature]]
    all_metric_df.append(metric_df)

all_metric_df = pd.concat(all_metric_df, axis=1)
metric_save_path = '%s/log_valid/metric.csv' % base_conf['base_dir']
all_metric_df.to_csv(metric_save_path)


#%%

#
# print('MSE', MSE(y_gt, y_predict))
# print('RMSE', RMSE(y_gt, y_predict))
#
# print('MAE', MAE(y_gt, y_predict))
# print('MAPE', MAPE(y_gt, y_predict))
# print('R2', R2(y_gt, y_predict))

# mape_perc = MAPE_percentage(y_gt, y_predict)





# %%
actual, predict = y_gt, y_predict
a = np.mean(np.abs((actual - predict) / actual), axis=1)
b = np.percentile(a,50)

#%%

#
# plt.figure(figsize=(10, 5))  # 设置画布的尺寸
# plt.title('Examples of boxplot', fontsize=20)  # 标题，并设定字号大小
#
# # boxprops：color箱体边框色，facecolor箱体填充色；
# plt.boxplot([box_1, box_2, box_3, box_4], patch_artist=True, boxprops={'color': 'orangered', 'facecolor': 'pink'})
#
# plt.show()  # 显示图像


