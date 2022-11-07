#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022-11-07 13:30
# @Site    :
# @File    : updateSpider.py
# @Software: PyCharm
import datetime
import os
import configparser  # 这个用于读取文件，写入文件会将中文注释删除
from XZGUtil.logger import conlog
from XZGUtil.timeUtil import get_now_date, getdate
from configobj import ConfigObj

proDir = os.path.split(os.path.realpath(__file__))[0]


class upconfig(object):
    def __init__(self, path=None, file_name="update", update_tag='spiderState'):
        """
        :param file_name:  文件名
        :param update_tag:   标签名
        """
        self.updatePath = os.path.join(path if path else proDir, f"{file_name}.ini")
        self.config = configparser.RawConfigParser()
        self.config.read(self.updatePath, encoding="utf-8-sig")
        self.set_config = ConfigObj(self.updatePath, encoding="utf-8-sig")
        self.update_tag = update_tag

    def get_information(self, name):
        """
        获取更新日期
        :param name:
        :return:
        """
        try:
            data = self.config.get(self.update_tag, f'{name}')
        except:
            data = None
        return data

    def set_information(self, name, date=get_now_date()):
        """
        修改更新日期配置文件
        :param name: 标签下的具体类名
        :return:
        """
        try:
            self.set_config[self.update_tag][f'{name}'] = date
        except KeyError:
            with open(self.updatePath, 'a') as f:
                f.write(f"[{self.update_tag}]")
            self.set_config = ConfigObj(self.updatePath, encoding="utf-8-sig")
        self.set_config[self.update_tag][f'{name}'] = date
        self.set_config.write()
        conlog(f'{self.update_tag}   *   {name}  *   ', f"更新完成_{date} ")


    def check_update(self, name):
        """
        检查今日是否更新
        :param name: 检查对象
        :return:
        """
        try:
            value = self.config.get(self.update_tag, f'{name}')
        except:
            try:
                self.config.set(self.update_tag, f'{name}', getdate(1))  # 如果报错说明没有这个则需要创建一个，并赋值为前一日
            except configparser.NoSectionError:
                with open(self.updatePath, 'a') as f:
                    f.write(f"[{self.update_tag}]")
                self.config.read(self.updatePath, encoding="utf-8-sig")
                self.config.set(self.update_tag, f'{name}', getdate(1))
            self.config.write(open(self.updatePath, 'w', encoding='utf-8-sig'))
            value = self.config.get(self.update_tag, f'{name}')
        if value == get_now_date():  # 更新日期为今日则停止更新
            conlog(f'{name}', "今日已更新完成")
            return False
        else:
            return True


if __name__ == '__main__':
    print(upconfig(update_tag = 'spiderSt33ate').set_information('答复9'))
    # print( QNActuator().get_information('spiderState', 'ylmf_sd'))
    # print(QNActuator().get_information('mysql', 'uuuu'))
    # print(QNActuator().get_information('spiderState', 'ylmf_dlr'))
