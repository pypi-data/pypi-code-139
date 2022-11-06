# Importing modules
import os
import shutil
import numpy as np

def rgb2hex(r:int, g:int, b:int) :
    """
    Converts RGB color code to hexadecimal
    @params:
        r    - Required  : Green channel (uint8)
        g    - Required  : Green channel (uint8)
        b    - Required  : Green channel (uint8)
    """
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


def hex2rgb(hexcode:str):
    """
    Converts hexadecimal color code to RGB
    @params:
        hexcode    - Required  : Hexadecimal code (Str)
    """
    return tuple(map(ord, hexcode[1:].decode('hex')))

# Function to convert binary to decima. This is used to obtain a single number for all the exclusion criteria (0: No exclusion)
def binaryToDecimal(a:int, b:int, c:int, d:int):
    """
    Converts 4bits binary number to decimal.. unction to convert binary to decimal.
    This is used to obtain a single number for all the exclusion criteria (0: No exclusion)
    @params:
        a    - Required  : Hexadecimal code (Str)
    """
    decimal = a*pow(2, 3) + b*pow(2, 2) + c*pow(2, 1) + d*pow(2, 0)
    return decimal

# Delete all the files inside a folder
def delete_files_folder(newPath:str):
    """
    Recursive deleting files in a specified folder)
    @params:
        InputDir    - Required  : Root directory (Str)
    """
    # Deleting all the files in a folder
    for file in os.listdir(newPath):
        file_path = os.path.join(newPath, file)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

# Function to detect all the files inside a directory
def detect_recursive_files(InputDir:str):
    """
    Function to detect all the files inside a directory
    @params:
        InputDir    - Required  : Root directory (Str)
    """

    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(InputDir):
        for file in f:
            files.append(os.path.join(r, file))
    return files


def removeDuplicates(s:str, dchar:str):
    """
    Function to remove certain adjacent duplicates characters from a string
    @params:
        s        - Required  : String (Str)
        dchar    - Required  : Character to look for (Str)
    """
    chars = []
    prev = None

    for c in s:
        if c != dchar:
            chars.append(c)
            prev = c
        else:
            if prev != c:
                chars.append(c)
                prev = c

    return ''.join(chars)

# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

def my_ismember(a, b):
    """
    Find elements of vector b in vector a
    @params:
        a   - Required  : Target vector
        b   - Required  : Values vector
    """
    values, indices = np.unique(a, return_inverse=True)
    is_in_list = np.isin(a, b)
    idx = indices[is_in_list].astype(int)

    return values, idx