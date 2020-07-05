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
    owner = None
    permission = None
    create_date = None
    update_date = None
    path = str()

    def __init__(self,name,size,owner,permission=755,parent_path=""):
        self.name = name
        self.size = size
        self.permission = permission
        self.owner = owner
        self.create_date = time.time()
        self.update_date = time.time()
        self.path = parent_path + "/" + name

class File(Object):
    content = None

    def __init__(self,name,size,owner,permission,parent_path=""):
        super().__init__(name,size,owner,permission,parent_path)
        self.content = str()

class Folder(Object):
    child_list = list()
    child_num = 0

    def __init__(self,name,size,owner,permission,parent_path=""):
        super().__init__(name,size,owner,permission,parent_path)
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
        
        print(inputData.args)

        try:
            dir_name = inputData.args[0]
        except IndexError as e:
            dir_name = ""
            print(e)
        
        if dir_name == ".":
            pass

        elif dir_name == "..":
            dir_list = self.current.path.split("/")
            self.current = self.root 
            for i in dir_list:
                if i == "root":
                    continue
                # if i == "":
                #     continue
                inputData.args[0] = i
                self.cd(inputData)
            
        elif dir_name == "~":
            self.current = self.root 
            inputData.args[0] = self.user.name
            self.cd(inputData)

        elif dir_name == "/":
            self.current = self.root

        elif isPath(dir_name):
            #절대경로
            if dir_name[0] == "/":
                self.current = self.root
                dir_list = dir_name[1:].split("/")
                for i in dir_list:
                    inputData.args[0] = i
                    self.cd(inputData)
            #상대경로
            else :
                dir_list = dir_name.split("/")
                for i in dir_list:
                    inputData.args[0] = i
                    self.cd(inputData)

        else :
            match_obj = None

            for i in self.current.child_list:
                if dir_name == i.name:
                    match_obj = i

            if match_obj is None:
                print("there is no such dir")
                    # there is no such dir. define noSuchDirError(07/02)
                    # raise ValueError
                raise ValueError
            
            if isDir(i):
                self.current = match_obj
            else:
                print("it is not dir")
                # it is not dir. define NotDirError(07/02)
                # raise ValueError
                raise ValueError
    
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
                
                _dir = Folder(name = i,size = 0,owner = self.user,permission = 755,parent_path = self.current.path)
                self.current.addFolder(_dir)
        
            print("owner : ",_dir.owner)
            print("permission : ",_dir.permission)

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
