# -*- coding: UTF-8 -*-

#import sys

#sys.path.append("../../")

import fire

from imca_frame.FileModule import FileBuilderClass
from imca_frame.InfoMan import InfoManClass
from imca_frame.SearchPkgModule import SearchPkgClass
import os
import yaml

class imca:
    
    def list_pkg(self):
        InfoManClass.INFO_NOTE(">> 搜索功能包...")
        flag = SearchPkgClass.search_pkg()
        if(flag != 0):
            InfoManClass.INFO_ERR("<< X 搜索失败")
        else:
            InfoManClass.INFO_NOTE(">> 搜索成功")

    def help(self):
        print("""
imca help                       查看帮助
     list-pkg                   列出所有功能包
     create workspace           创建工作空间
            pkg --name=<包名>   创建功能包
        """)

    class create:

        def __init__(self):
            self.file_builder = FileBuilderClass()
            pass

        def pkg(self, name):
            InfoManClass.INFO_NOTE(">> 创建功能包: {0}".format(name))
            flag = self.file_builder.createPKG(name)
            if(flag != 0):
                InfoManClass.INFO_ERR("<< X 创建功能包失败")
            else:
                InfoManClass.INFO_NOTE(">> 成功功能包")

            RM_PATH = os.environ.get("RM_PATH")
            yaml_list = FileBuilderClass.getYamlPath()
            if(len(yaml_list) <= 0):
                return -10
            list_context = ""
            for path in yaml_list :
                path += "/.Config.yaml"
                with open(path, "r", encoding="utf-8") as f:
                    result = yaml.load(f.read(), Loader=yaml.FullLoader)
                    list_context += result["module_name"] + " "
            
            if(RM_PATH != None):
                config_file = open(RM_PATH + "/script/ModuleList.txt", "w")
            config_file.write(list_context[0:-1])
            config_file.close()


        def workspace(self):
            InfoManClass.INFO_NOTE(">> 创建工作空间")
            flag = self.file_builder.createWorkSpace()
            if(flag != 0):
                InfoManClass.INFO_ERR("<< X 创建工作空间失败")
            else:
                InfoManClass.INFO_NOTE(">> 成功创建工作空间")


def main():
    fire.Fire(imca)
    pass

if __name__ == '__main__':
    main()
