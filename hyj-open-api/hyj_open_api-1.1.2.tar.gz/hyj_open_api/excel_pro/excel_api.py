import openpyxl
import HuYuJiePythonApi.python_auto as auto
import copy

def choose_many_file_mix_keywords_list_(file_keyword_dict):
    mixed_names = list()  # 记录所有欲合成文件的关键词
    final_names = list()  # 记录传入的字典最后一个键值对所遍历出excel的值
    object_names = list()  # 深度复制final_name
    for i, count in zip(file_keyword_dict, range(len(file_keyword_dict))):
        sheet = openpyxl.load_workbook(i).active
        names = auto.ExcelApi(sheet).find_cols_by_name(file_keyword_dict[i])
        if count != len(file_keyword_dict) - 1:
            mixed_names.append(names)
        else:
            final_names = names
            object_names = copy.deepcopy(final_names)
    for o in final_names:
        for nums in range(len(mixed_names)):
            for num in mixed_names[nums]:
                if num == o:
                    object_names.remove(num)
    return object_names