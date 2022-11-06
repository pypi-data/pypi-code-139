from time import time
from os import mkdir, environ, listdir, remove
from typing import List, final
from json import load, dump
from io import TextIOWrapper

__MAX_CACHE_FILES__: int = environ.get("MAX-CACHE-FILES", 3)
__CACHE_FOLDER__: str = environ.get("CACHE-FOLDER", ".cache")


class Cacheable(object):
    __cache_file_hook__: TextIOWrapper
    
    def __init__(self) -> None:
        try:    mkdir(".cache")
        except: ...
        files: List[str] = []
        for file in listdir(".cache"):
            if file.startswith(f'{self.__class__.__name__}'):
                files.append(file)
        stamps: List[int] = [ int(file.split("-")[1].split(".")[0]) for file in files ]
        stamps.sort()
        
        result_file: List[str] = []
        
        # Sorting for getting the latest file
        for file in files:
            for stamp in stamps:
                if file.count(f'{stamp}') == 1:
                    result_file.append(file)
        
        if len(result_file) == 0:
            self.__cache_file_hook__ = open(f'{__CACHE_FOLDER__}/{self.__free_file__()}', 'x')
            return
        
        with open(f'{__CACHE_FOLDER__}/{result_file[0]}', 'r') as cache_file:
            self.__dict__ = load(cache_file)
            self.__cache_file_hook__ = open(f'{__CACHE_FOLDER__}/{self.__free_file__()}', 'x')

    @final
    @classmethod
    def __free_file__(cls) -> str:
        return f'{cls.__name__}-{int(time())}.json'

    @final
    @classmethod
    def __clean_cache_files__(cls):
        files: List[str] = []
        for file in listdir(".cache"):
            if file.startswith(f'{cls.__name__}'):
                files.append(file)

        # File overflow
        if len(files) > __MAX_CACHE_FILES__ - 1:
            stamps: List[int] = [ int(file.split("-")[1].split(".")[0]) for file in files ]
            stamps.sort()
            for file in files:
                if len(files) == __MAX_CACHE_FILES__ - 1:
                    break
                for stamp in stamps:
                    if file.count(f'{stamp}') == 1:
                        files.remove(file)
                        stamps.remove(stamp)
                        remove(f'{__CACHE_FOLDER__}/{file}')
                        break
        
    def __del__(self):
        self.__clean_cache_files__()

        passed = self.__dict__.copy()
        try:    passed.pop('__cache_file_hook__')
        except: ...

        dump(passed, self.__cache_file_hook__)
        self.__cache_file_hook__.close()
