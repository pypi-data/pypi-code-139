# -*- coding: UTF-8 -*-

'''
    命令格式：可执行文件 <create | list> <workspace | pkg> <name>
'''

from imca_frame.InfoMan import InfoManClass
from imca_frame.FileModule import FileBuilderClass
from imca_frame.SearchPkgModule import SearchPkgClass
import os
import yaml

# 处理命令类
class ComDealClass:

    #argc = 0
    #argv = []

    #comm_format = "命令格式：可执行文件 <create | list> <workspace | pkg> <name>"

    def __init__(self, argc, argv):
        self.argc = argc
        self.argv = argv
        self.comm_format = "命令格式：可执行文件 <create | list> <workspace | pkg> <name>"
        self.file_builder = FileBuilderClass()

        pass

    def com_deal(self):
        if(self.argc <= 1):
            InfoManClass.INFO_ERR(">> X 没有参数. -> " + self.comm_format)
            return -1
        
        if(self.argv[1] == "create"):
            if(self.argc <= 2):
                InfoManClass.INFO_ERR(">> X 参数异常. -> " + self.comm_format)
                return -2
            elif(self.argc > 2 and self.argv[2] == "workspace"):
                if(self.argc > 3):
                    InfoManClass.INFO_ERR(">> X workspace语法错误. ->" + self.comm_format)
                    return -3
                else:
                    InfoManClass.INFO_NOTE(">> 正在创建工作空间...")
                    flag = self.file_builder.createWorkSpace()
                    if(flag == 0):
                        InfoManClass.INFO_NOTE("<< 工作空间创建完毕, 请载入setup.sh脚本")
                    else:
                        InfoManClass.INFO_ERR("<< X 工作空间创建失败")
            elif(self.argc > 2 and self.argv[2] == "pkg"):
                if(self.argc != 4):
                    InfoManClass.INFO_ERR("Xworkspace语法错误. ->" + self.comm_format)
                    return -4
                elif(self.argc == 4):
                            
                    InfoManClass.INFO_NOTE(">> 正在创建功能包 : " + self.argv[3])
                    flag = self.file_builder.createPKG(self.argv[3])
                    if(flag != 0):
                        InfoManClass.INFO_ERR("<< X 创建功能包" + self.argv[3] + "失败")
                    else:
                        InfoManClass.INFO_SUCC("<< 功能包 " + self.argv[3] + " 创建成功")
                
            else:
                InfoManClass.INFO_ERR("<< X 语法错误. ->" + self.comm_format)
        elif(self.argv[1] == "list" and self.argc == 2):
            SearchPkgClass.search_pkg()
            pass
        else:
            InfoManClass.INFO_ERR("<< X 语法错误. ->" + self.comm_format)


        yaml_list = FileBuilderClass.getYamlPath()
        if(len(yaml_list) <= 0):
            return -10

        list_context = ""

        for path in yaml_list :
            path += "/.Config.yaml"
            with open(path, "r", encoding="utf-8") as f:
                result = yaml.load(f.read(), Loader=yaml.FullLoader)
                list_context += result["module_name"] + " "

        RM_PATH = os.environ.get("RM_PATH")
        if(RM_PATH != None):
            config_file = open(RM_PATH + "/script/ModuleList.txt", "w")
        config_file.write(list_context[0:-1])
        config_file.close()
        return 0
        

