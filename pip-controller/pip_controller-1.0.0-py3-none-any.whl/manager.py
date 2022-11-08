import os
import sys
import logging
from typing import List
from sys import platform

__all__ = [
    "install",
    "uninstall",
]

class _controller:
    def __init__(self, package_list:List[str], upgrade:bool=False, abs_path:str="", python_cmd:str=None):

        if python_cmd == None : 
            if platform == "linux" or platform == "linux2":
                self.cmd = "python3"
            elif platform == "darwin":
                self.cmd = "python3"
            elif platform == "win32":
                self.cmd = "python"
        else : 
            self.cmd = python_cmd

        if upgrade == True:
            self.upgrade = "--upgrade"
        else: 
            self.upgrade = ""

        self.package_names = package_list
        
        if abs_path != "": os.makedirs(abs_path, exist_ok=True)
        self.pip_path = os.path.join(abs_path, "pip_list.txt")
        os.system(f"{self.cmd} -m pip list >> "+ self.pip_path.replace(" ", "\ "))
        os.system(f"{self.cmd} -m pip install --upgrade pip")
        with open(f"{self.pip_path}", "r", encoding="utf-8-sig") as f:
            self.lines = f.readlines()
        
    def install(self):
        for package_name in self.package_names:
            check_intalled = False
            for search in self.lines: 
                check_intalled = check_intalled or search.split(' ')[0].lower()==package_name.lower()
            if(check_intalled is False): 
                os.system(f"{self.cmd} -m pip install {self.upgrade} {package_name}")
                logging.debug(f"install {self.upgrade} {package_name}")
        os.remove(f"{self.pip_path}")
    
    def uninstall(self):
        for package_name in self.package_names:
            check_intalled = False
            for search in self.lines: 
                check_intalled = check_intalled or search.split(' ')[0].lower()==package_name.lower()
            if(check_intalled is True): 
                os.system(f"{self.cmd} -m pip uninstall -y {package_name}")
                logging.debug(f"uninstall {package_name}")
        os.remove(f"{self.pip_path}")

class install(_controller):
    def __init__(self, package_names: List[str], upgrade: bool = False, abs_path: str = "", python_cmd: str = None):
        super().__init__(package_names, upgrade, abs_path, python_cmd)
        super().install()

class uninstall(_controller):
    def __init__(self, package_names: List[str], upgrade: bool = False, abs_path: str = "", python_cmd: str = None):
        super().__init__(package_names, upgrade, abs_path, python_cmd)
        super().uninstall()

# test code
if __name__ == "__main__":

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(filename)s | %(funcName)s | %(message)s ')

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)
    
    file_handler = logging.FileHandler("logs.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)

    install(package_names=["kivy", "kivymd"], upgrade=True, python_cmd="python3.10")
    uninstall(package_names=["kivy", "kivymd"], python_cmd="python3.10")