import os

from pyipcore.ipb import *
import pyperclip

class IPCoreReBuilder:
    def __init__(self, ipc_path, work_path) -> None:
        self.f_ips = files(ipc_path, ".pyip")
        self.content = None

        # -------------------
        self._dir_path = os.path.dirname(__file__)
        self._ipc_path = ipc_path
        self._work_path = work_path

        # ---------------------
        self.reset()

    def reset(self):
        self.fvda   = None
        self.vars   = None
        # self.nida   = None
        self.nivars = None
        self.dfda   = None
        self.dfvars = None
        self.hlpda  = None
        self.hlpvars = None
        self.fnda   = None
        self.rfnvars = None
        self.fda    = None
        self.inst_code = None
        self.kvs = {}
        self.rf_kvs = {}
        self._rebuild = None
        self.attr_fda = None
        self.dfvars = None

    def loadIPCore(self, ipc_name) -> bool:
        # Load IP core content
        self.reset()
        content = self.f_ips.get(ipc_name)
        if not content: 
            try:
                content = LoadIp(os.path.join(self._ipc_path, ipc_name + ".v"))
            except FileNotFoundError as err:
                print(f"{err}\n\n[ERROR]: No such file or directory")
                return
        self.content = content
        return True
    
    def closeIPCore(self):
        self.content = None
        self.reset()

    def checkContent(self):
        if self.content is None:
            raise NoContentException("Please call '.loadIPCore(name)' first")
            return False
        return True

    def analyseVariables(self):
        self.checkContent()
        try:
            self.fvda  = FindAll("\$\w+", self.content)  # find $xxx
            self.vars = list(set([each[1] for each in self.fvda]))  # [string like $xxx]

        except Exception as err:
            print(f"{err}\n\n[ERROR]: Failed to load $VARIABLE")
            return 

    def analyseVariables_Defaults(self):
        self.checkContent()
        try:
            self.dfda  = FindAll("//\s*\$\w+\s*=.*", self.content)  # find // $xxx = 
            self.dfvars = {}  # [string like $xxx: string value]
            for df in self.dfda:
                k = re.search("\$\w+", df[1]).group()
                v = re.search("=.*", df[1]).group()[1:]
                v = re.sub("^\s*", "", v)
                self.dfvars[k] = v
        except Exception as err:
            print(f"{err}\n\n[ERROR]: Failed to load $VARIABLE:DEFAULT")
            return 

    # def analyseVariables_WhichNoInputs(self):
    #     self.checkContent()
    #     try:
    #         self.nida  = FindAll("//\s*\^\$\w+[:\s].*", self.content)  # find // ^$xxx
    #         self.nivars = []  # [string like $xxx]
    #         for ni in self.nida:
    #             k = re.search("\$\w+", ni[1]).group()
    #             self.nivars += [k]
    #     except Exception as err:
    #         print(f"{err}\n\n[ERROR]: Failed to load $VARIABLE:NO-INPUT")
    #         return

    def analyseVariables_Helps(self):
        self.checkContent()
        try:
            self.hlpda   = FindAll("//\s*h\$\w+\s*[=:]?\s*.*", self.content)  # find // h$xxx:
            self.hlpvars = {}  # {string like $xxx: string help}
            for hlp in self.hlpda:
                span, k = FindAll("\$\w+", hlp[1])[0]
                left = re.sub("^\s", "", hlp[1][span[1]:])  # remove all \s at first
                if left[0] in [":", "="]:
                    left = re.sub("^\s", "", left[1:])
                self.hlpvars[k] = left
        except Exception as err:
            print(f"{err}\n\n[ERROR]: Failed to load $VARIABLE:HELP")
            return 

    def analyseVariables_Refuncs(self):
        self.checkContent()
        try:
            self.fnda   = FindAll("//\s*\^?f\$\w+\s*[=:]?\s*.*", self.content)  # find // f$xxx:
            self.rfnvars = {} # raw fnvars
            self.fnvars = {}  # {string like $xxx: string help}
            self.nivars = []
            for fn in self.fnda:
                span, k = FindAll("\$\w+", fn[1])[0]
                left = re.sub("^\s", "", fn[1][span[1]:])  # remove all \s at first
                if left[0] in [":", "="]:
                    left = re.sub("^\s", "", left[1:])
                self.rfnvars[k] = left
                self.fnvars[k]  = left.replace("$", "")
                ########################
                if fn[1][fn[1].find("f") - 1] == "^":
                    self.nivars += [k]
        except Exception as err:
            print(f"{err}\n\n[ERROR]: Failed to load $VARIABLE:FUNC")
            return 

    def analyseInstCode(self):
        self.checkContent()
        try:
            self.fda = FindAll("/\*[^\*]+\*/", self.content)
            if len(self.fda) == 0:
                self.inst_code = f"{self.ipc_name}();"
                print(f"[WARNING]: Can not find INST_CODE")
            else: 
                self.inst_code = self.fda[-1][1]
                self.inst_code = self.inst_code[2:-2]
        except Exception as err:
            print(f"{err}\n\n[ERROR]: Failed to load INST_CODE")
            return 

    def analyseAll(self) -> None:
        self.analyseVariables()
        self.analyseVariables_Defaults()
        self.analyseVariables_Helps()
        self.analyseVariables_Refuncs()
        self.analyseInstCode()

    def getVariable_Help(self, var_name, none_value=None) -> str:
        if self.hlpvars is None:
            raise NoAnalyseHelpException("Please call '.analyseVariables_Helps()' first")
        if var_name[0] != "$":
            var_name = "$" + var_name
        return self.hlpvars.get(var_name, none_value)

    def getVariables_Helps(self) -> dict:
        if self.hlpvars is None:
            raise NoAnalyseHelpException("Please call '.analyseVariables_Helps()' first")
        return self.hlpvars.copy()

    def getVariable_Default(self, var_name, none_value=None) -> str:
        if self.dfvars is None:
            raise NoAnalyseDefaultException("Please call '.analyseVariables_Defaults()' first")
        if var_name[0] != "$":
            var_name = "$" + var_name
        return self.dfvars.get(var_name, none_value)

    def getVariables_Defaults(self) -> dict:
        if self.dfvars is None:
            raise NoAnalyseDefaultException("Please call '.analyseVariables_Defaults()' first")
        return self.dfvars.copy()

    def getVariables(self) -> list:
        if self.fvda is None:
            raise NoAnalyseVariablesException("Please call '.analyseVariables()' first")
        return self.vars.copy()

    def getVariables_RawRefuncs(self) -> dict:
        """
        like {$xxx: string}
        """
        if self.rfnvars is None:
            raise NoAnalyseRefuncVariablesException("Please call '.analyseVariables_Refuncs()' first")
        return self.rfnvars.copy()

    def getVariables_Refuncs(self) -> dict:
        """
        like {$xxx: string(remove $)}
        """
        if self.fnvars is None:
            raise NoAnalyseRefuncVariablesException("Please call '.analyseVariables_Refuncs()' first")
        return self.fnvars.copy()

    def getVariables_WhichNeedInputs(self) -> list:
        ndi_vars = []
        for k in self.vars:
            if self.nivars is not None and k in self.nivars: continue
            # if k in self.kvs.keys(): continue
            ndi_vars += [k]
        return ndi_vars

    def getVariables_WhichNoInputs(self):
        if self.nivars is None:
            raise NoAnalyseVariablesException("Please call '.analyseVariables_Refuncs()' first")
        return self.nivars.copy()

    def getVariables_WhichUnfilled(self):
        uf_vars = []
        for k in self.vars:
            if self.nivars is not None and k in self.nivars: continue
            if k in self.kvs.keys(): continue
            uf_vars += [k]
        return uf_vars 
    
    def getVariables_WhichInputed(self, var_name):
        if self.kvs is None:
            raise NoFillVariablesException("Please call '.fillVariables(kvs)' first")
        if var_name[0] != "$":
            var_name = "$" + var_name
        return self.kvs.get(var_name)

    def getVariable_Value(self, var_name, none_value = None):
        if self.kvs is None:
            raise NoFillVariablesException("Please call '.fillVariables(kvs)' first")
        if var_name[0] != "$":
            var_name = "$" + var_name
        if self.rf_kvs is not None:
            if var_name in self.rf_kvs:
                return self.rf_kvs[var_name]
        return self.kvs.get(var_name, none_value)

    def getVariables_Values(self):
        kvs = {}
        if self.kvs is not None:
            for k in self.kvs:
                kvs[k] = self.kvs[k]
        if self.rf_kvs is not None:
            for k in self.rf_kvs:
                kvs[k] = self.rf_kvs[k]
        return kvs

    def getInstCode(self):
        if self.inst_code is None:
            raise NoInstCodeException("Please call '.analyseInstCode(kvs)' first")
        
        fda = FindAll("\$\w+", self.inst_code)
        kvs = self.getVariables_Values()

        _ric, last = "", 0
        for each in fda:
            _ric += self.inst_code[last: each[0][0]]
            try:
                _ric += kvs[each[1]]
            except KeyError as err:
                print(f"{err}\n\n[ERROR]: can not find a value to replace {each[1]}")
                return 

            last = each[0][1]
        _ric += self.inst_code[last:]
        return _ric

    def getRebuild(self):
        return self._rebuild


    def fillVariables(self, kvs):
        """
        kvs: {$var: input value}
        """
        self.kvs.update(kvs)

    def refuncVariables(self):
        if self.kvs is None:
            raise NoFillVariablesException("Please call '.fillVariables(kvs)' first")
        if self.fvda is None:
            raise NoAnalyseVariablesException("Please call '.analyseVariables()' first")
        if self.fnvars is None or self.rfnvars is None:
            raise NoAnalyseRefuncVariablesException("Please call '.analyseVariables_Refuncs()' first")

        ns_kvs = {k[1:]:v for k, v in self.kvs.items()}  # no $ version
        pre_fns = GetPreFunctions()
        self.rf_kvs = {}
        for each in self.fvda:
            rfn_string = self.rfnvars.get(each[1], each[1])
            fn_string  = self.fnvars.get(each[1], each[1][1:])  # simplified fn do not contain $
            # print(each[1])
            nkms = NsKvsMask(each[1], rfn_string, ns_kvs)
            nkms.update(pre_fns)
            # print(nkms)
            #try: 
            self.rf_kvs[each[1]] = str(eval(fn_string, nkms))
            #except Exception as err:
            #    print(f"{err}\n\n[ERROR]: Failed to refunc {each[1]}")
             #   return 

    def doRebuild(self):
        self.checkContent()
        if self.fvda is None:
            raise NoAnalyseVariablesException("Please call '.analyseVariables()' first")

        kvs = self.getVariables_Values()

        self._rebuild, last = "\n", 0
        for each in self.fvda:
            self._rebuild += self.content[last: each[0][0]]

            try:
                self._rebuild += kvs[each[1]]
            except KeyError as err:
                print(f"{err}\n\n[ERROR]: can not find a value to replace {each[1]}")
                return 

            last = each[0][1]
        self._rebuild += self.content[last:]

    def removeNotes(self):
        """
        won't remove inst_code at file end.
        """
        if self._rebuild is None:
            raise NoRebuildException("Please call '.rebuild()' first")

        self._rebuild = re.sub("\n//.*", "", self._rebuild)
        while self._rebuild[0] == '\n': self._rebuild = self._rebuild[1:]

    def buildVariablesValueNote(self):
        if self._rebuild is None:
            raise NoRebuildException("Please call '.rebuild()' first")

        input_note = f"// INPUT: \n{self.kvs}\n" if self.kvs is not None else ""
        rf_note = f"// REFUNC: \n{self.rf_kvs}\n" if self.rf_kvs is not None else ""

        total_note = "/*\n"
        total_note += input_note if input_note != "" else ""
        total_note += rf_note if rf_note != "" else ""
        total_note += "*/\n"

        return total_note

    def addVariablesValueNote(self):
        self._rebuild = self.buildVariablesValueNote() + self._rebuild

    def doDefaultRebuild(self, ipc_name):
        """
        quick rebuild a version by default value.
        """
        
        if not self.loadIPCore(ipc_name): return
        ##################################################################
        # analyse $xxx
        self.analyseVariables()  # essential!

        # analyse $xxx
        self.analyseVariables_Defaults()  # essential!

        # analyse function for $xxx
        self.analyseVariables_Refuncs()


        df_vars = self.getVariables_Defaults()

        self.fillVariables(df_vars)

        if temp:=self.getVariables_WhichUnfilled():
            print(f"[ERROR]: No default value for {temp} in '{ipc_name}'")
            return False

        self.refuncVariables()

        self.doRebuild()
        return True
    def saveAs(self, path):
        if self._rebuild is None:
            raise NoRebuildException("Please call '.rebuild()' first")
        SaveIp(self._rebuild, path)

    def save(self, name):
        self.saveAs(os.path.join(self._work_path, name + ".v"))


def build(rebuilder:IPCoreReBuilder, ipc_name):
    if ipc_name.lower() in ["quit", "exit"]:
        exit(0)

    if not rebuilder.loadIPCore(ipc_name): return
    ##################################################################
    # analyse $xxx
    rebuilder.analyseVariables()  # essential!

    # analyse $xxx
    rebuilder.analyseVariables_Defaults()  # essential!

    # analyse help for $xxx
    rebuilder.analyseVariables_Helps()

    # analyse function for $xxx
    rebuilder.analyseVariables_Refuncs()

    # analyse instiation code last /* */
    rebuilder.analyseInstCode()

    ##################################################################
    # Fill $xxx value
    i, kvs  = 0, {}
    uf_vars = rebuilder.getVariables_WhichUnfilled()
    #print(uf_vars)
    print("Fill Params:")
    for k in uf_vars:
        if (hlp:=rebuilder.getVariable_Help(k)):  # Need rebuilder.analyseVariables_Helps()
            print(f"\thelp{hlp}")    # help if have
        
        default = rebuilder.getVariable_Default(k)
        default_txt = f" (default={default})" if default is not None else ""
        print(f"\t{i}. {k[1:]}{default_txt}: ", end="")  # k = $xxx

        get = input()
        if get == "": 
            print(f"-- USE DEFAULT({default}) --")
            kvs[k] = default
        else: kvs[k] = get

        i += 1
        print()
    rebuilder.fillVariables(kvs)

    # refunction and rebuild
    rebuilder.refuncVariables()
    rebuilder.doRebuild()
    rebuilder.removeNotes()
    rebuilder.addVariablesValueNote()

    new_file_name = rebuilder.getVariable_Value("$module_name")
    if new_file_name is None:
        new_file_name = input("New file name: ")

    rebuilder.save(new_file_name)
    
    print("---- DONE ----")
    pyperclip.copy(rebuilder.getInstCode())
    print("---- COPY INST_CODE TO CLIPBOARD ----\n")

def IPRebuild(work_path = None, ipc_path = None):
    print("// enter 'quit' or 'exit' to stop\n")
    if (ipc_path is None): ipc_path = input("> IPCore Source Directory: ")
    if ipc_path.lower() in ["quit", "exit"]:
        exit(0)
    if (work_path is None): work_path = input("> Work Path: ")
    if work_path.lower() in ["quit", "exit"]:
        exit(0)
    rebuilder = IPCoreReBuilder(ipc_path, work_path)
    while 1:
        build(rebuilder, input("> Ip name: "))

if __name__ == "__main__":
    # Test Unit
    # C:\Users\CIE2018\Desktop\pyip\test_temp
    
    IPRebuild(r"C:\Users\CIE2018\Desktop\pyipcore\test_temp", r"C:\Users\CIE2018\Desktop\pyipcore\ipcore")
