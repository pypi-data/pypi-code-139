import os
import json, jsonlines
from collections import OrderedDict, defaultdict
from typing import List, Union


def create_dirs_if_not_exist(path: str):
    """Create the directory where the path points to.
    Does nothing if the dir already exists

    Args:
        path (str): Either a path to a directory or a file
    """
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


def load_json(path: str):
    """Loads the json file from 'path' into a list of dicts

    Args:
        path (str): The path to the json file

    Raises:
        ValueError: If the provided path does not point to a json file

    Returns:
        dict: A dict of the json file
    """
    if not ".json" in path:
        raise ValueError("'path' is not pointing to a json file")
    data = None
    with open(path) as f:
        data = json.loads(f.read())
    return data


def load_jsonl(path: str) -> List[dict]:
    """Loads the jsonl file from 'path' into a list of dicts

    Args:
        path (str): The path to the jsonl file

    Raises:
        ValueError: If the provided path does not point to a jsonl file

    Returns:
        List[dict]: A list of the jsonl file
    """
    if not ".jsonl" in path:
        raise ValueError("'path' is not pointing to a jsonl file")
    result = []
    with jsonlines.open(path) as reader:
        for doc in reader:
            result.append(doc)
    return result


def load_txt(path: str):
    """Loads the text file from 'path' into a list of strings

    Args:
        path (str): The path to the text file

    Raises:
        ValueError: If the provided path does not point to a text file

    Returns:
        List[str]: A list of strings from the text file
    """
    if not ".txt" in path:
        raise ValueError("'path' is not pointing to a text file")
    data = None
    with open(path) as f:
        data = f.read().splitlines()
    return data

def store_json(
    data: Union[dict, list, defaultdict, OrderedDict],
    file_path: str,
    sort_keys=False,
    indent=2,
    verbose=True
):
    """ Function for storing a dict to a json file. 
        Will create the directories in the path if they don't
        already exist.

    Args:
        data (dict): The dict or list to be stored in the json file
        file_path (str): The path to the file to be created (note: will delete files that have the same name)
        sort_keys (bool, optional): Set to True if the keys in the dict should be sorted before stored (default: False)
        indent (bool, optional): Set this if indentation should be added (default: None)
        verbose (bool, optional): If True, will print a message with the path to the file when stored. Defaults to True.

    Raises:
        ValueError: If the input datatype is not correct or the file path does not point to a json file
    """
    if (
        type(data) != dict
        and type(data) != list
        and type(data) != defaultdict
        and type(data) != OrderedDict
    ):
        raise ValueError("'data' needs to be a dict")
    if ".json" not in file_path:
        raise ValueError("'file_path' needs to include the name of the output file")
    create_dirs_if_not_exist(file_path)
    with open(file_path, mode="w") as f:
        f.write(json.dumps(data, sort_keys=sort_keys, indent=indent))
    if verbose:
        print(f"Stored data to '{file_path}'")


def store_jsonl(data: list, file_path: str, verbose=True):
    """ Function for storing a list as a jsonl file.
        Will create the directories in the path if they don't
        already exist.

    Args:
        data (list): A list of arbitrary type
        file_path (str): The path to the file to be created (note: will delete files that have the same name)
        verbose (bool, optional): If True, will print a message with the path to the file when stored. Defaults to True.

    Raises:
        ValueError: If the input datatype is not correct or the file path does not point to a jsonl file
    """
    if type(data) != list:
        raise ValueError("'data' needs to be a list")
    if ".jsonl" not in file_path:
        raise ValueError("'file_path' needs to include the name of the output file")
    create_dirs_if_not_exist(file_path)
    with jsonlines.open(file_path, mode="w") as f:
        for d in data:
            f.write(d)
    if verbose:
        print(f"Stored data to '{file_path}'")


def store_multiple_json(
    data: List[dict], 
    file_names: List[str],
    sort_keys=False,
    indent=2,
    verbose=True
):
    """Stores multiple dicts to json files.
    The number of dicts and file names must be the same.

    Args:
        data (List[dict]): A list of dicts to be stored
        file_names (List[str]): A list of file names where the dicts should be stored
        sort_keys (bool, optional): If True, will sort the keys of the dicts. Defaults to False.
        indent (int, optional): The indent to use when storing the dicts. Defaults to 2.
        verbose (bool, optional): If True, will print a message with the path to the files when stored. Defaults to True.
    """
    if len(data) != len(file_names):
        raise ValueError("The number of dicts and file names must be the same")
    for i, d in enumerate(data):
        store_json(
            data=d,
            file_path=file_names[i],
            sort_keys=sort_keys,
            indent=indent,
            verbose=verbose
        )
      
      
def store_txt(data: List[str], file_path: str, verbose=True):
    """Stores a list of strings to a text file, 
    each element separated by a newline.

    Args:
        data (List[str]): A list of strings to be stored in the text file
        file_path (str): A path to the text file
        verbose (bool, optional): If True, will print a message with the path to the file when stored. Defaults to True.
    """
    if type(data) != list:
        raise ValueError("'data' needs to be a list")
    if ".txt" not in file_path:
        raise ValueError("'file_path' needs to include the name of the output file and it needs to be a '.txt' file")
    create_dirs_if_not_exist(file_path)
    with jsonlines.open(file_path, mode="w") as f:
        for d in data:
            f.write(d)
    if verbose:
        print(f"Stored data to '{file_path}'")
    

def unique(sequence: list):
    """Returns all the unique items in the list while keeping order (which set() does not)
       Also works for list of dicts

    Args:
        sequence (list): The list to filter

    Returns:
        list: List with only unique elements
    """    
    unique_list = list()
    for x in sequence:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list
