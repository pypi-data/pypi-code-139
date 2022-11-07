from genericpath import isdir
import os
from posixpath import join
from typing import List


class FileUtil:

    LOCALOZABLE_PATH = "/.tdf_tools/localizable"
    LOCAL_STRING_TYPES = [
        "en",
        "zh-Hans",
        "zh-Hant",
        "th",
    ]

    def localizable_path() -> str:
        return os.path.expanduser("~") + FileUtil.LOCALOZABLE_PATH

    def get_allfile(path, suffix_str_list=[]) -> list[str]:
        if isdir(path) == False:
            print("不存在路径：" + path)
            return []
        all_file = []
        for (root, dirs, files) in os.walk(path):
            for f in files:
                for suffix_str in suffix_str_list:
                    if f.endswith(suffix_str):
                        all_file.append(join(root, f))
        return all_file
