# -*- coding:utf-8 -*-
import os
import re
import sys
from files3 import files
from pyverilog.vparser.ast import *
from pyverilog.vparser.parser import VerilogParser
font_path = os.path.join(os.getenv("SystemDrive"), "Windows", "Fonts", "simhei.ttf")

IPCTYPE = ".pyipc"

def LoadIp(path):
    """
    load .pyipc or .v
    """
    temp = os.path.splitext(path)
    name, type = os.path.split(temp[0])[1], temp[1]
    dir = os.path.split(path)[0]

    if type.lower() == IPCTYPE:
        return files(dir, IPCTYPE).get(name)
    else:
        return open(path, 'r').read()


def SaveIp(content, path):
    """
    save .pyipc or .v
    """
    temp = os.path.splitext(path)
    name, type = os.path.split(temp[0])[1], temp[1]
    dir = os.path.split(path)[0]

    if type.lower() == IPCTYPE:
        return files(dir, IPCTYPE).set(name, content)
    else:
        return open(path, 'w').write(content)


def FindAll(pattern, content, empty_error=0, keep_empty=0):
    """
    return [(span, string), ...]
    empty_error: whether error when null 
    keep_empty: (empty_error == 0), whether save it?
    """
    result, offset = [], 0
    while len(content):
        match = re.search(pattern, content, re.I)
        if match is not None:
            span = match.span()
            result.append(([span[0] + offset, span[1] + offset], content[span[0]: span[1]]))
            
            if (span[1] - span[0]) == 0:
                if empty_error: 
                    raise(Exception(f"[ERROR]:Get span({span[0] + offset}, {span[1] + offset}), which content nothing. \n\nPlease check and update your pattern and retry."))
                if not keep_empty:
                    result.pop(-1)

                print(f"[WARNING]:Get span({span[0] + offset}, {span[1] + offset}), which content nothing. Will auto shift by 1 char after it.")
                span = (span[0], span[1] + 1)
                offset += 1

            offset += span[1]
            content = content[span[1]:]
        else:
            break
    return result 

# def KvsMask(var_name, raw_fn_string, kvs):
#     fda = FindAll("\$\w+", raw_fn_string)
#     kvs_masked = {var_name}
#     for each in fda:
#         try:
#             kvs_masked[each[1]] = kvs[each[1]]
#         except KeyError:
#             raise KeyError(f"Can not find {each[1]} for f{var_name} = {raw_fn_string}")
#     return kvs_masked

# nskvs: (no $)var_name:value
def NsKvsMask(raw_var_name, raw_fn_string, ns_kvs):
    fda = FindAll("\$\w+", raw_fn_string)
    ns_kvs_masked = {}
    for each in fda:
        each = each[1][1:]
        try:
            ns_kvs_masked[each] = ns_kvs[each]
        except KeyError:
            raise KeyError(f"Can not find {each} for f{raw_var_name} = {raw_fn_string}")
    return ns_kvs_masked

def AstInstanceFilter(ast:Node, instances:list, data_passby:dict=None):
    if not isinstance(ast, Node): return {}
    childs = ast.children()
    if data_passby is None:
        data_passby = {}
    
    for each in instances:
        if isinstance(ast, each): 
            if data_passby.get(each) is not None:
                data_passby[each].append(ast)
            else:
                data_passby[each] = [ast]
            break

    for child in childs:
        AstInstanceFilter(child, instances, data_passby)
    
    return data_passby

def CalcScale(size_from, size_to_fit):
    a = size_to_fit[0] - size_from[0]
    b = size_to_fit[1] - size_from[1]
    if a > b:  # indicate that width will left blank
        scale = size_to_fit[1] / size_from[1]
    else:
        scale = size_to_fit[0] / size_from[0]
    return scale

class NoContentException(Exception): ...

class NoAnalyseHelpException(Exception): ...

class NoAnalyseVariablesException(Exception): ...

class NoAnalyseRefuncVariablesException(Exception): ...

class NoRebuildException(Exception): ...

class NoFillVariablesException(Exception): ...

class NoInstCodeException(Exception): ...

class NoAnalyseDefaultException(Exception): ...


class IOInfos:
    def __init__(self, name, type, width, reg) -> None:
        self.name = name
        self.type = type
        self.type_name = type.__class__.__name__.lower()
        self.width = width
        self.reg   = reg

    def __str__(self) -> str:
        _type = f"{self.type_name} " if self.type is not None else ""
        _reg = "reg " if self.reg is not None else ""
        _width = f"[{self.width.msb}:{self.width.lsb}] " if self.width is not None else ""
        return _type + _reg + _width + self.name
    
    def __repr__(self) -> str:
        return str(self)
        

class IPCoreParse:
    def __init__(self, parse_ast) -> None:
        self.ast = parse_ast

        result = AstInstanceFilter(self.ast, [ModuleDef, Paramlist, Portlist])
        self.module_name = result.get(ModuleDef, ["UNKNOWN"])[0]
        if isinstance(self.module_name, ModuleDef):
            self.module_name = self.module_name.name
        
        self.params = {}
        paramslist = result.get(Paramlist, [None])[0]
        if paramslist is not None:
            params = AstInstanceFilter(paramslist, [Parameter, ]).get(Parameter, [])
            for param in params:
                values = AstInstanceFilter(param, [Rvalue, ])  # Only support int value
                value = values.get(Rvalue, [None])[0]
                if value is not None:
                    self.params[param.name] = int(value.var.value)
        
        self.ports = {}
        portslist = result.get(Portlist, [None])[0]
        if portslist is not None:
            ports = AstInstanceFilter(portslist, [Ioport, ]).get(Ioport, [])
            for port in ports:
                infos  = AstInstanceFilter(port, [Inout, Input, Output, Width, Reg])  # Only support int value
                reg    = infos.get(Reg,   [None])[0]
                input  = infos.get(Input, [None])[0]
                output = infos.get(Output, [None])[0]
                inout  = infos.get(Inout, [None])[0]
                width  = infos.get(Width, [None])[0]

                if inout is not None:
                    self.ports[inout.name] = IOInfos(inout.name, inout, width, reg)
                elif input is not None:
                    self.ports[input.name] = IOInfos(input.name, input, width, reg)
                elif output is not None:
                    self.ports[output.name] = IOInfos(output.name, output, width, reg)


    def getModuleName(self):
        return self.module_name
    
    def getParams(self):
        return self.params
    
    def getPorts(self):
        return self.ports


class Environ: ...

_env = None
def CreateEnviron():
    global _env
    _env = Environ()

    for each in f_env.list():
        setattr(_env, each, f_env[each])



def GetEnviron():
    if _env is None:
        CreateEnviron()
    return _env

f_env = files('', ".envkey")
def SaveEnvrionKey(key):
    f_env[key] = getattr(GetEnviron(), key, None)

###############################################

def GetBit(integer) -> int:
    """
    Get the length by binary of an integer
    will auto int(param).
    """
    return len(bin(int(integer))[2:])

_prefns = None
def CreatePreFunctions():
    global _prefns
    _prefns = {}
    _prefns["GetBit"] = GetBit

def GetPreFunctions():
    if _prefns is None:
        CreatePreFunctions()
    return _prefns



if __name__ == "__main__":
    a = LoadIp("counter.v")
    a = FindAll("\$\w*", a)
    print(a)

