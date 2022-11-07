# -*- coding: UTF-8 -*-

import os
from imca_frame.InfoMan import InfoManClass
import datetime as dt
import pwd
import yaml
from enum import Enum

class YAML_MODE(Enum):
    ROOT = 1
    PKG = 2

class FileBuilderClass:

    cur_path = ""

    def __init__(self):
        path = str(os.popen("pwd").readline())
        self.cur_path = path[0 : len(path) - 1]
        self.author = "// create by " + pwd.getpwuid( os.getuid())[0] + "\t " + str(dt.datetime.now().strftime('%F %T') + "\n")
        
    # 获取当前Bash路径
    def get_cur_path(self):
        path = str(os.popen("pwd").readline())
        return path[0 : len(path) - 1]

    # 创建YAML文件
    def createYAML(self, m_name, mode):
        RM_PATH = os.environ.get("RM_PATH")
        if(RM_PATH is None):
            return -1
        author = pwd.getpwuid( os.getuid())[0]
        create_time = str(dt.datetime.now().strftime('%F %T'))
        if(mode == YAML_MODE.ROOT):
            yaml_type = "root"
        elif(mode == YAML_MODE.PKG):
            yaml_type = "pkg"
        
        infoData = {
            "module_name": m_name,
            "author": author,
            "create_time": create_time,
            "type" : yaml_type,
            "descripe": ""
        }
        if(mode == YAML_MODE.ROOT):
            with open(RM_PATH + "/src/" + m_name + "/." + "Config" + ".yaml", "w", encoding="utf-8") as f:
                yaml.dump(data=infoData, stream=f, allow_unicode=True)
        elif(mode == YAML_MODE.PKG):
            with open(RM_PATH + "/src/" + m_name + "/." + "Config" + ".yaml", "w", encoding="utf-8") as f:
                yaml.dump(data=infoData, stream=f, allow_unicode=True)

        InfoManClass.INFO_SUCC(">> 成功创建YAML")
        return 0
        
    # 写YAML 文件
    def readYAML(self, f_name):
        with open(self.cur_path + "/" + f_name, "r", encoding="utf-8") as f:
            #InfoManClass.INFO_NOTE(self.cur_path + "/Test.yaml")
            result = yaml.load(f.read(), Loader=yaml.FullLoader)
            return result

    # 获取YAML路径
    @staticmethod
    def getYamlPath():
        RM_PATH = os.environ.get("RM_PATH")
        yaml_list = []
        if(RM_PATH != None):
            for root, dirs, files in os.walk(RM_PATH + "/src"):
                for name in files:
                    file_path = os.path.join(root, name)
                    if(".yaml" in file_path):
                        yaml_list.append(root)
        return yaml_list

    # 创建根CMakeLists.txt
    def createRootCmakeList(self):
        cmake_context = [
            "# Root\n",
            "# cmake版本\n",
            "cmake_minimum_required(VERSION 3.17)\n",
            "# 项目名\n"
            "project(ROOT_IMCA)\n",
            "# C++ 版本\n",
            "set(CMAKE_CXX_STANDARD 14)\n",
            "# 添加头文件目录\n",
            "include_directories(${PROJECT_SOURCE_DIR}/src/)\n",
            "# 搜索Python3",
            "set(PYTHON3_EXECUTABLE \"/usr/bin/python3\")",
            "# 环境初始化\n",
            "execute_process(COMMAND ${PYTHON3_EXECUTABLE} get_module_list.py WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}/script)\n",
            "# 读取功能包列表\n",
            "file(READ ${PROJECT_SOURCE_DIR}/script/ModuleList.txt read_file_var)\n"
            "# Set Submodule BEGIN\n",
            "set(Module_Lists ${read_file_var})\n",
            "separate_arguments(Module_Lists)\n",
            "foreach(sub_name IN LISTS Module_Lists)\n",
            "\tmessage(SubModuleName: ${sub_name})\n",
            "\tmessage(SubModulePath: ${PROJECT_SOURCE_DIR}/src/${sub_name})\n",
            "\tadd_subdirectory(${PROJECT_SOURCE_DIR}/src/${sub_name})\n",
            "endforeach()\n",
            "# Set Submodule END\n",
            "# 查找当前目录下的SRC文件\n",
            "aux_source_directory(. DIR_SRCS)\n",
            "# 添加到可执行文件\n",
            "add_executable(${PROJECT_NAME} ${DIR_SRCS})\n",
            "# Third Model BEGIN\n",
            "foreach(sub_name IN LISTS Module_Lists)\n",
            "\tstring(FIND ${sub_name} \"/\" sub_pos REVERSE)\n",
            "\tif(${sub_pos} GREATER -1)\n",
            "\t\tmath(EXPR sub_pos \"${sub_pos} + 1\" OUTPUT_FORMAT DECIMAL)\n",
            "\t\tmessage(Sub_Pos: ${sub_pos})\n",
            "\t\tstring(SUBSTRING ${sub_name} ${sub_pos} -1 sub_name)\n",
            "\tendif()\n",
            "\ttarget_link_libraries(${PROJECT_NAME} ${sub_name})\n",
            "endforeach()\n",
            "# Third Model END\n",
            "# 从此处自定义连接第三方库\n"
        ]
        cmakeListWriter = open(self.cur_path + "/CMakeLists.txt", "w")
        cmakeListWriter.writelines(cmake_context)
        InfoManClass.INFO_SUCC(">> 成功创建CMakeLists.txt")
        cmakeListWriter.close()

    # 创建工作空间
    def createWorkSpace(self):
        if(len(os.listdir(self.cur_path)) > 0):
            InfoManClass.INFO_ERR(">> X 当前文件不为空")
            return -1
        
        RM_PATH = os.environ.get("RM_PATH")
        if((RM_PATH != None) and RM_PATH in self.cur_path):
            InfoManClass.INFO_ERR(">> X 无法在工作空间下重复创建工作空间")
            return -2

        src_dir = self.cur_path + "/src"
        if(os.path.exists(src_dir)):
            InfoManClass.INFO_ERR(">> X src 文件夹已存在")
        else:
            os.makedirs(src_dir) 
            InfoManClass.INFO_SUCC(">> 成功创建SRC文件夹")
 
        script_dir = self.cur_path + "/script"
        if(os.path.exists(script_dir)):
            InfoManClass.INFO_ERR(">> X script 文件夹已存在")
        else:
            os.makedirs(script_dir)
            InfoManClass.INFO_SUCC(">> 成功创建script文件夹")
        
        write_main = open(self.cur_path + "/main.cpp", "w")
        
        main_context = [
            self.author,
            "// 头文件包含区 BEGIN\n", 
            "\n", 
            "// 头文件包含区 END\n", 
            "\n", 
            "int main(int argc, char ** argv){\n",
            "\t// 在此编写代码 BEGIN\n",
            "\n",
            "\t// 在此编写代码 END\n",
            "\treturn 0;\n",
            "}\n"]


        """
        main.cpp 内容

        // 头文件包含区 BEGIN

        // 头文件包含区 END

        int main(int argc, char ** argv){
            // 在此编写代码 BEGIN

            // 在此编写代码 END
            return 0;
        }

        """

        write_main.writelines(main_context)
        InfoManClass.INFO_SUCC(">> 成功创建Main")
        write_main.close()

        # 脚本，用于shell初始化
        export_sh = open(script_dir + "/setup.sh", "w")
        export_sh.write("unset RM_PATH\n")
        export_sh.write("export RM_PATH=" + self.cur_path)
        InfoManClass.INFO_SUCC(">> 成功创建启动脚本")
        export_sh.close()

        # 记录功能包列表
        ModuleList_txt = open(script_dir + "/ModuleList.txt", "w")
        InfoManClass.INFO_SUCC(">> 成功创建包名单")
        ModuleList_txt.close()

        python_file = open(script_dir + "/get_module_list.py", "w")
        python_file.write("""import os
import yaml

RM_PATH = {0}
config_file = open(RM_PATH + "/script/ModuleList.txt", "w")
yaml_list = []
if(RM_PATH != None):
    for root, dirs, files in os.walk(RM_PATH + "/src"):
        for name in files:
            file_path = os.path.join(root, name)
            if(".yaml" in file_path):
                yaml_list.append(file_path)

list_context = ""

for path in yaml_list :
    with open(path, "r", encoding="utf-8") as f:
        result = yaml.load(f.read(), Loader=yaml.FullLoader)
        list_context += RM_PATH + "/src/" + result["module_name"] + " "

config_file.write(list_context[0:-1])
config_file.close()
print("\\033[0;32m>>读取成功<<\\033[0m")
        """.format("\"" + self.cur_path + "\""))
        python_file.close()

        self.createRootCmakeList()
        self.createYAML("RM_Root", YAML_MODE.ROOT)
        return 0


    # 创建子CMAKE
    def createPkgCMakeList(self, root_path, module_name):
        cmake_file_path = root_path + "/CMakeLists.txt"
        cmake_file = open(cmake_file_path, "w")
        cmake_file_context = [
            "# 功能包名\n",
            "project(" + module_name + ")\n",
            "# 搜索.cpp文件的所有路径\n",
            "FILE(GLOB_RECURSE CPP_SET ${PROJECT_SOURCE_DIR} *.cpp)\n",
            "# 搜索.h文件的所有路径\n"
            "FILE(GLOB_RECURSE H_SET ${PROJECT_SOURCE_DIR} *.h)\n\n",
            "message(\"SRC_SET = \" ${CPP_SET})\n",
            "message(\"H_SET = \" ${H_SET})\n",
            "# 添加头文件路径\n",
            "include_directories(${PROJECT_SOURCE_DIR}/inc/)\n",
            "add_library(${PROJECT_NAME} ${CPP_SET} ${H_SET})\n"
        ]
        cmake_file.writelines(cmake_file_context)
        cmake_file.close()
        InfoManClass.INFO_SUCC(">> 成功创建功能包 " + module_name + " 的CMakeLists.txt")
        pass

        
    # 创建功能包
    def createPKG(self, p_name):

        yaml_list = self.getYamlPath()
        bash_cur = self.get_cur_path()

        # InfoManClass.INFO_NOTE(str(yaml_list))

        for yaml_file in yaml_list:
            if(yaml_file in bash_cur):
                InfoManClass.INFO_ERR(">> X 不能在功能包里创建功能包")
                return -1

        RM_PATH = os.environ.get("RM_PATH")
        if(RM_PATH == None):
            InfoManClass.INFO_ERR(">> X 未找到工作空间")
            return -2

        if((RM_PATH + "/src") not in bash_cur):
            InfoManClass.INFO_ERR(">> X 不再当前工作空间")
            return -3
        
        root_path = bash_cur + "/" + p_name
        src_path = root_path + "/src"
        inc_path = root_path + "/inc"
        if(os.path.exists(src_path)):
            InfoManClass.INFO_ERR(">> X src 文件夹已存在")
        else:
            os.makedirs(src_path) 
            InfoManClass.INFO_SUCC(">> 成功创建SRC文件夹")

        if(os.path.exists(inc_path)):
            InfoManClass.INFO_ERR(">> X inc 文件夹已存在")
        else:
            os.makedirs(inc_path) 
            InfoManClass.INFO_SUCC(">> 成功创建INC文件夹")

        src_file_name = p_name + ".cpp"
        inc_file_name = p_name + ".h"

        src_file_path = src_path + "/" + src_file_name
        src_file = open(src_file_path, "w")
        src_file_context = [
            self.author,
            "#include \"../inc/" + inc_file_name + "\"\n",
            "\n",
            "void " + p_name + "::to_string(){\n",
            "\tprintf(\"This Class Name : " + p_name + "\");\n",
            "}\n"
        ]
        src_file.writelines(src_file_context)
        src_file.close()

        InfoManClass.INFO_SUCC(">> 成功创建" + src_file_name)

        inc_file_path = inc_path + "/" + inc_file_name
        inc_file = open(inc_file_path, "w")
        inc_file_context = [
            self.author,
            "#ifndef " + p_name.upper() + "__H__\n",
            "#define "+ p_name.upper() + "__H__\n",
            "#include <cstdio>\n"
            "\n",
            "class " + p_name + "{\n",
            "private:\n",
            "\t// 存放私有变量\n",
            "\n",
            "public:\n",
            "\t// 存放公共函数\n",
            "\tvoid to_string();\n"
            "\n",
            "};\n",
            "#endif\n"
        ]
        inc_file.writelines(inc_file_context)
        inc_file.close()

        InfoManClass.INFO_SUCC(">> 成功创建" + inc_file_name)
        self.createPkgCMakeList(root_path, p_name)
        if(bash_cur[len(RM_PATH + "/src/"):] == ""):
            module_name = p_name
        else:
            module_name = bash_cur[len(RM_PATH + "/src/"):] + "/" + p_name
        self.createYAML(module_name, YAML_MODE.PKG)

        return 0


