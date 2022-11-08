#!/usr/bin/env python3
import os

def list_non_hidden_content(option:int = 1) -> list:
    """
    Note: Default parameter (option) of 1 in effect if no other is supplied
    Note: This function was created with Linix and Mac users in mind

    Takes an int value of either 1 or 2 which is expressed as options

    option 1: returns either a list of all non hidden [directories + files] 
    option 2: a list of lists of non hidden [directories , files]
    """
    dir_path = "."
    hidden_files = ['.', '~$', "Icon\r"]
    cwd = [i for i in os.listdir(
        dir_path) if not i.startswith(tuple(hidden_files))]
    dirs = [i for i in cwd if os.path.isdir(dir_path+os.sep+i)]
    files = [i for i in cwd if not os.path.isdir(dir_path+os.sep+i)]
    
    if option == 1:
        return dirs+files
    elif option == 2:
        return [dirs, files]
    else:
        raise ValueError("parameters must be of type int and can only be either 1 or 2")


if '__name__' == "__main__":
    exit(list_non_hidden_content())