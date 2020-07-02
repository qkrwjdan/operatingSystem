import time
from userExceptions import *

def isPath(string_obj):
    if '/' in string_obj:
        return 1
    return 0

def isDir(dir_or_file_obj):
    if str(type(dir_or_file_obj)) == "<class 'objects.Folder'>":
        return 1
    return 0

def isFile(dir_or_file_obj):
    if str(type(dir_or_file_obj)) == "<class 'objects.File'>":
        return 1
    return 0

class User:
    name = None
    pwd = None

    def __init__(self,name,pwd):
        self.name = name
        self.pwd = pwd

class Object:
    name = None
    size = None
    create_date = None
    update_date = None
    path = str()

    def __init__(self,name,size,path=""):
        self.name = name
        self.size = size
        self.create_date = time.time()
        self.update_date = time.time()
        self.path = path + "/" + name

class File(Object):
    content = None

    def __init__(self,name,size,path=""):
        super().__init__(name,size,path)
        self.content = str()

class Folder(Object):
    child_list = list()
    child_num = 0

    def __init__(self,name,size,path=""):
        super().__init__(name,size,path)
        self.child_list = list()
        self.child_num = 0

    def addFolder(self,sub_directory):
        self.child_list.append(sub_directory)
        self.child_num = self.child_num + 1

class ObjectHandler:

    def __init__(self,root,user):
        self.root = root
        self.user = user
        self.current = root

    def cd(self,inputData):

        if len(inputData.args) > 1:
            #define user error (07/02)
            raise ValueError

        dir_name = inputData.args[0]
        
        if dir_name == ".":
            print(dir_name)

        elif dir_name == "..":
            print(dir_name)

        elif dir_name == "~":
            print(dir_name)
            self.current = self.root 
            inputData.args[0] = "park"
            return self.cd(inputData)

        elif dir_name == "/":
            print(dir_name)
            self.current = self.root

        elif isPath(dir_name):
            print(dir_name)
            dir_list = dir_name.split("/")
            for i in dir_list:
                self.cd(i)

        else :
            print(dir_name)
            for i in self.current.child_list:
                if  dir_name == i.name:
                    if isDir(i):
                        self.current = i
                    
    
    def ls(self,inputData):
        for i in self.current.child_list:
            print(i.name,end = " ")
            
        print()

    def pwd(self,inputData):
        if inputData.option is not None:
            print("pwd : {option} : invalid option ".format(inputData.option))
        else:
            print(self.current.path)

    def mkdir(self,inputData):
        if inputData.option is None:
            for i in inputData.args:

                if isPath(i):
                    raise FileOrFolderNameError("directory name is path")

                for j in self.current.child_list:
                    if i == j.name:
                        raise FileOrFolderNameError("same directory is exist")
                    
                _dir = Folder(i,0,self.current.name)
                self.current.addFolder(_dir)

        elif inputData.option == "-p":
            pass

        elif inputData.option == "-m":
            pass

        else:
            pass

    def rm(self,inputData):
        pass

    def cp(self,inputData):
        pass

    def cat(self,inputData):
        pass

    def find(self,inputData):
        pass
