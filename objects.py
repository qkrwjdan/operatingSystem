import time
from userExceptions import *
from sys import getsizeof
from input import InputData

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

def intToPermissionString(one_digit):
    if one_digit == 7:
        return "wrx"
    elif one_digit == 6:
        return "wr-"
    elif one_digit == 5:
        return "w-x"
    elif one_digit == 4:
        return "w--"
    elif one_digit == 3:
        return "-rx"
    elif one_digit == 2:
        return "-r-"
    elif one_digit == 1:
        return "--x"

def getPermissionStr(int_permission):
    owner_permission = int(int_permission / 100)
    group_permission = int(int_permission / 10) % 10
    etc_permission = int_permission % 10

    permission_str = intToPermissionString(owner_permission) + intToPermissionString(group_permission) + intToPermissionString(etc_permission)
    return permission_str

def isDirOrFileReturnStr(dir_or_file_obj):
    if isDir(dir_or_file_obj):
        return "d"
    elif isFile(dir_or_file_obj):
        return "-"
    else:
        return "l"

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

    def __init__(self,name,owner,permission=755,parent_path=""):
        self.name = name
        self.size = getsizeof(self)
        self.permission = permission
        self.owner = owner
        self.create_date = time.time()
        self.update_date = time.time()
        self.path = parent_path + "/" + name

class File(Object):
    content = None

    def __init__(self,name,owner,permission,parent_path=""):
        super().__init__(name,owner,permission,parent_path)
        self.content = str()

class Folder(Object):
    child_list = list()
    child_num = 0

    def __init__(self,name,owner,permission,parent_path=""):
        super().__init__(name,owner,permission,parent_path)
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
            print("dir_list : ",dir_list)
            self.current = self.root 
            for i in dir_list[:-1]:
                if i == "":
                    continue
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
                raise NoSuchDirectoryError
            
            if isDir(i):
                self.current = match_obj
            else:
                print("it is not dir")
                # it is not dir. define NotDirError(07/02)
                # raise ValueError
                raise ValueError
    
    def ls(self,inputData):

        #ls -l path를 구현하기
        #현재는 current directory만 출력가능 (07/06)

        if inputData.option == "-a":
            for i in self.current.child_list:
                print(i.name,end = " ")
            print()

        elif inputData.option == "-l":
            print("permission linkNum user group size date name")
            for i in self.current.child_list:
                if i.name.startswith("."):
                    continue
                print(isDirOrFileReturnStr(i),getPermissionStr(i.permission),2,i.owner.name,"staff",i.size,i.update_date,i.name)

        elif inputData.option == "-al":
            print("permission linkNum user group size date name")
            for i in self.current.child_list:
                print(isDirOrFileReturnStr(i),getPermissionStr(i.permission),2,i.owner.name,"staff",i.size,i.update_date,i.name)

        elif inputData.option == "-ll":
            print("permission linkNum user group size date name")
            for i in self.current.child_list:
                if i.name.startswith("."):
                    continue
                print(isDirOrFileReturnStr(i),getPermissionStr(i.permission),2,i.owner.name,"staff",i.size,i.update_date,i.name)

        else:
            for i in self.current.child_list:
                if i.name.startswith("."):
                    continue
                print(i.name,end = " ")
            print()

    def pwd(self,inputData):
        if inputData.option is not None:
            print("pwd : {option} : invalid option ".format(inputData.option))
        else:
            if self.current == self.root:
                print("/")
            else :
                print(self.current.path)

    def mkdir(self,inputData):
        if inputData.option is None:
            for i in inputData.args:

                if isPath(i):
                    raise FileOrFolderNameError("directory name is path")

                for j in self.current.child_list:
                    if i == j.name:
                        raise FileOrFolderNameError("same directory is exist")
                
                _dir = Folder(name = i,owner = self.user,permission = 755,parent_path = self.current.path)
                self.current.addFolder(_dir)
        
            print("owner : ",_dir.owner)
            print("permission : ",_dir.permission)

        elif inputData.option == "-p":

            for i in inputData.args:
                if not isPath(i):
                    print("wrong input")
                    raise ValueError

                if not i[0] == "/":
                    print("wrong path")
                    raise ValueError

                dir_list = i[1:].split("/")
                print(dir_list)

                if self.current == self.root:
                    temp_path = "/"
                else :
                    temp_path = self.current.path

                temp_input = InputData(["cd","/"])
                self.cd(temp_input)

                for i in dir_list:
                    print(dir_list)
                    print("i : ",i)
                    try:
                        tmp = InputData(["mkdir",i])
                        self.cd(tmp)
                    except NoSuchDirectoryError :
                        self.mkdir(tmp)
                        self.cd(tmp)
                
                print("temp_path : ", temp_path)
                self.cd(InputData(["cd",temp_path]))

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
