# -*- coding: utf-8 -*-
# @Organization  : TMT
# @Author        : Cuong Tran
# @Time          : 11/7/2022
import os
import random
import shutil
from multiprocessing import Process


def _move_files_list(data, src, dst):
    for idx, d in enumerate(data):
        path_ori_data = os.path.join(src, d)
        shutil.copy(path_ori_data, dst)


def folder_dataset_split(root_path, dst_path, ratio_train=0.8):
    os.makedirs(dst_path, exist_ok=True)
    os.makedirs(os.path.join(dst_path, 'train'), exist_ok=True)
    os.makedirs(os.path.join(dst_path, 'test'), exist_ok=True)

    clss = os.listdir(root_path)
    for cls in clss:
        path = os.path.join(root_path, cls)
        if os.path.isdir(path):
            new_train_path = os.path.join(os.path.join(dst_path, 'train', cls))
            new_test_path = os.path.join(os.path.join(dst_path, 'test', cls))
            os.makedirs(new_train_path, exist_ok=True)
            os.makedirs(new_test_path, exist_ok=True)

            data = os.listdir(path)
            random.shuffle(data)

            pivot = int(ratio_train * len(data))
            train_data = data[:pivot]
            test_data = data[pivot:]
            Process(target=_move_files_list, args=(train_data, path, new_train_path)).start()
            Process(target=_move_files_list, args=(test_data, path, new_test_path)).start()

            # for idx, d in enumerate(data):
            #     path_ori_data = os.path.join(path, d)
            #     path_dst_data = new_train_path if idx <= pivot else new_test_path
            #     shutil.copy(path_ori_data, path_dst_data)


if __name__ == '__main__':
    folder_dataset_split(r'F:\Zalo Live Face\image_224_dataset', r'F:\Zalo Live Face\image_224_dataset_split')
