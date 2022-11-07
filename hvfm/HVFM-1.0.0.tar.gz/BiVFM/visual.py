#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/18 18:42
# @Author  : 马赫
# @Email   : 1692303843@qq.com
# @FileName: visual.py

from BiVFM.train_func import *

import matplotlib.dates as mdates

base_yaml_path = 'olga_work1/conf_0_base.yaml'

base_conf = get_base_config(base_yaml_path)
# print(base_conf)

pkl_dir = base_conf['pkl_dir']
raw_data_list = pickle_load('%s/raw_data_list.pkl' % pkl_dir)


i_data = raw_data_list[0]
#%%

PT_Qowg_data = i_data

index_plt = PT_Qowg_data.index



fig = plt.figure(figsize=(10, 9), dpi=300)
ax1 = fig.add_subplot(2,1,1)

ax1.scatter(index_plt, PT_Qowg_data.loc[:, 'P_Mpa_choke_ahead'], c='#328655', s=1, label='P')
plt.xticks(rotation=25)
plt.legend(loc='upper left', fontsize='large', markerscale=5)
plt.ylabel('Pressure (MPa)')


ax12 = ax1.twinx()
ax12.scatter(index_plt, PT_Qowg_data.loc[:, 'T_C_choke_ahead'], c='#DF6223', s=1, label='T')

plt.xlim([index_plt[0], index_plt[-1]])
# fig.legend(loc=(0.12, 0.8))
plt.legend(loc='upper right', fontsize='large', markerscale=5)
plt.ylabel('Temperature (℃)')

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%M:%S'))


ax2 = fig.add_subplot(2,1,2)
plt.xticks([])


# b #203A97
# r #DF6223
# g #328655
# yellow #F4C944



ax2.scatter(index_plt, PT_Qowg_data.loc[:, 'QO'], c='#328655', s=1, label='$Q_o$')
ax2.scatter(index_plt, PT_Qowg_data.loc[:, 'QW'], c='#203A97', s=1, label='$Q_w$')
plt.title('Time')

plt.ylabel('$Q_o, Q_w (m^3/d)$')

plt.legend(loc='upper left', fontsize='large', markerscale=5)

ax21 = ax2.twinx()
ax21.scatter(index_plt, PT_Qowg_data.loc[:, 'QG'], c='#DF6223', s=1, label='$Q_g$')

plt.xlim([index_plt[0], index_plt[-1]])
# fig.legend(loc=(0.09, 0.75))
plt.legend(loc='upper right', fontsize='large', markerscale=5)
plt.ylabel('$Q_g (m^3/d)$')

plt.savefig('draw_PTQ.jpg', dpi=300, bbox_inches='tight')

plt.show()




