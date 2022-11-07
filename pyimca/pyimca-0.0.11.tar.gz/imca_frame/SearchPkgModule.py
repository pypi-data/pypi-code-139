from imca_frame.InfoMan import InfoManClass
import os
import yaml
from imca_frame.FileModule import FileBuilderClass

class SearchPkgClass:
    @staticmethod
    def search_pkg():
        RM_PATH = os.environ.get("RM_PATH")
        if(RM_PATH == None):
            InfoManClass.INFO_ERR(">> X 未找到工作空间")
            return -1

        yaml_list = FileBuilderClass.getYamlPath()
        InfoManClass.INFO_NOTE("<< 搜索完成：共{0}条记录".format(str(len(yaml_list))))

        for cur_file in yaml_list:
            yaml_file = cur_file + "/.Config.yaml"
            with open(yaml_file, "r", encoding="utf-8") as f:
                result = yaml.load(f.read(), Loader=yaml.FullLoader)
                print("包名 : %s\t\t作者 : %s\t\t创建时间 : %s\t\t描述 : %s\n\t>>> 所在路径 : %s" %(result["module_name"], result["author"], result["create_time"], result["descripe"], yaml_file))
                print("------------------------------------------------------")

        return 0
