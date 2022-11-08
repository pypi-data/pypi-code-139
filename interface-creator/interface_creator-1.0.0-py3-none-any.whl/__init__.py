import ast
import typing
import os

class InterfaceCreator:
    """
    this class loads a module from a file path and creates an interface mirroring all the methods, classes and attributes
    """
    def __init__(
        self, 
        filePath: str, 
        targetPath : str=None,
        ignoreDecorators : bool=True,
        enforcedDecorators : typing.List[str]=["cached_property"],
        formatSource : bool=False,
        skipLocalImports : bool=True
    ) -> None:
        if not os.path.exists(filePath):
            raise FileNotFoundError("file path does not exist")

        self.filePath = filePath
        self.fileSource = None
    
        with open(self.filePath, "r") as file:
            self.fileSource = file.read()
        
        if targetPath is None:
            return 
    
        self.baseAstTree = ast.parse(self.fileSource)
        
        self.ignoreDecorators = ignoreDecorators
        self.enforcedDecorators = enforcedDecorators
        self.formatSource = formatSource
        self.skipLocalImports = skipLocalImports
        
    def _create_class_interface(self, cls : ast.ClassDef, indent : int =0) -> str:
        ret_string = ""

        class_variables = [node for node in cls.body if isinstance(node, ast.AnnAssign)]    
        functions = [node for node in cls.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
        subclasses = [node for node in cls.body if isinstance(node, ast.ClassDef)]
        
        # create the class
        # check has inheritance
        if len(cls.bases) > 0:
            base_joins = ", ".join([base.id for base in cls.bases])
            ret_string += indent*"\t"
            ret_string += f'class {cls.name}({base_joins}):'
            ret_string += "\n"
        else:
            ret_string += (indent+1)*"\t"+ f"class {cls.name}:\n"
        
        ret_string += "\n"
        
        for subclass in subclasses:
            ret_string += self._create_class_interface(subclass, indent=indent+1)
        
        ret_string += "\n"
        
        for var in class_variables:
            # ast to source
            ret_string += (indent+1)*"\t"+ f"{ast.unparse(var)}\n"
                        
       
                        
        # all functions
        for func in functions:
            ret_string += "\n"
            
            # get the arguments
            args = [arg.arg for arg in func.args.args]
            # get the return type 
            returns = ast.unparse(func.returns) if func.returns is not None else "None"
            
            # check if static method
            if func.decorator_list and not self.ignoreDecorators:
                for decorator in func.decorator_list:
                    ret_string += (indent+1)*"\t"+f"@{ast.unparse(decorator)}\n"
            elif func.decorator_list:
                # still check static, class and property
                for decorator in func.decorator_list:
                    if decorator.id == "staticmethod":
                        ret_string += (indent+1)*"\t"+f"@staticmethod\n"
                    elif decorator.id == "classmethod":
                        ret_string += (indent+1)*"\t"+f"@classmethod\n"
                    elif decorator.id == "property":
                        ret_string += (indent+1)*"\t"+f"@property\n"     
                    elif decorator.id in self.enforcedDecorators:
                        ret_string += (indent+1)*"\t"+f"@{decorator.id}\n"
                    
                    
            # write the function
            ret_string += (indent+1)*'\t'
            # if async
            if isinstance(func, ast.AsyncFunctionDef):
                ret_string += "async "
            ret_string += f"def {func.name}({', '.join(args)})"
            if returns:
                ret_string += f" -> {returns}"
            ret_string += ":\n"
            ret_string += (indent+2)*"\t"+ f"pass\n"
        return ret_string
    
    def _create_imports(self) -> str:
        imports = [node for node in self.baseAstTree.body if isinstance(node, (ast.Import, ast.ImportFrom))]
        ret_string = ""
        
        # list all local folders
        local_folders = os.listdir(os.getcwd())
        
        for import_ in imports:
            # if imports name is from a local folder
            if self.skipLocalImports and import_.names[0].name in local_folders:
                continue
            
            if (
                isinstance(import_, ast.ImportFrom)
                and (import_package_name:= import_.module.split("."))
                and self.skipLocalImports 
                and import_package_name[0] in local_folders 
                and os.path.exists(os.path.join(os.getcwd(), *import_package_name[:-1]))
            ):
                continue
            
            ret_string +=f"{ast.unparse(import_)}\n"
        
        return ret_string
    
    @staticmethod
    def format_source(source : str) -> str:
        import autopep8
        return autopep8.fix_code(source, options={"aggressive": 2})
    
    def create(self) -> str:
        ret_string = ""
        ret_string += self._create_imports()
        ret_string += "\n"
        
        classes = [node for node in self.baseAstTree.body if isinstance(node, ast.ClassDef)]
        for cls in classes:
            ret_string += self._create_class_interface(cls)
        
        if self.formatSource:
            ret_string = self.format_source(ret_string)
        
        return ret_string
        
        
        
    @classmethod
    def createInterface(
        cls, 
        sourcePath : str,
        targetPath :str,
        ignoreDecorator : bool = True,
        enforcedDecorators : typing.List[str] = ["cached_property"],
        formatSource : bool = False,
        skipLocalImports : bool = True
    ) -> None:
        """
        creates an interface from a source string
        """
        interfaceCreator = cls(
            sourcePath, 
            targetPath, 
            ignoreDecorator, 
            enforcedDecorators, 
            formatSource,
            skipLocalImports
        )
        interface = interfaceCreator.create()
        
        with open(targetPath, "w") as file:
            file.write(interface)

                               


    