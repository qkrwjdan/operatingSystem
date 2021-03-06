import time
from userExceptions import *
from sys import getsizeof
from input import InputData

def isPath(string_obj):
    if '/' in string_obj:
        return 1
    elif string_obj == ".":
        return 1
    
    return 0

def isAbsPath(string_obj):
    if string_obj[0] == '/':
        return 1
    return 0

def isRelPath(string_obj):
    if not string_obj[0] == '/':
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

def dividePath(string_obj):
    path_list = string_obj.split("/")
    if isAbsPath(string_obj):
        return path_list[1:]
    else :
        return path_list

def transferPermisionIntToString(one_digit):
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

    permission_str = transferPermisionIntToString(owner_permission) + transferPermisionIntToString(group_permission) + transferPermisionIntToString(etc_permission)
    return permission_str

def isDirOrFileReturnStr(dir_or_file_obj):
    if isDir(dir_or_file_obj):
        return "d"
    elif isFile(dir_or_file_obj):
        return "-"
    else:
        return "l"

def checkPermissionValidation(int_permission):
    owner_permission = int(int_permission / 100)
    group_permission = int(int_permission / 10) % 10
    etc_permission = int_permission % 10

    if (owner_permission > 7) or (owner_permission < 0):
        raise ValueError
    
    if (group_permission > 7) or (group_permission < 0):
        raise ValueError

    if (etc_permission > 7) or (etc_permission < 0):
        raise ValueError

def isSafePath(directory,path_list):

    if not path_list:
        return 1

    for child in directory.child_list:
        if path_list[0] == child.name:
            return isSafePath(child,path_list[1:])
    
    return 0

def getSafePathFromPath(directory,path_list):

    return_string = "/"

    if not path_list:
        return ""
    
    for child in directory.child_list:
        if path_list[0] == child.name:
            return "/" + child.name + getSafePathFromPath(child,path_list[1:])
    
    return ""
    

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

    def __init__(self,name,owner,permission,parent_path,content):
        super().__init__(name,owner,permission,parent_path)
        self.content = content

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
    
    def deleteFile(self,file_obj):
        index = 0
        for ele in self.child_list:
            if ele.name == file_obj.name:
                del self.child_list[index]
                break
            index = index + 1


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
                print("there is no such dir")
                raise NoSuchDirectoryError
            
            if isDir(match_obj):
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
            # mkdir -m 824 
            # 명령어에 대한 예외처리 필(07/08)

            print(inputData.args)

            permission = inputData.args[0]

            try:
                int_permission = int(inputData.args[0])
                checkPermissionValidation(int_permission)
            except ValueError as e:
                print(e)
                return

            fileName = inputData.args[1]

            for i in inputData.args[1:]:

                if isPath(i):
                    raise FileOrFolderNameError("directory name is path")

                for j in self.current.child_list:
                    if i == j.name:
                        raise FileOrFolderNameError("same directory is exist")
                
                _dir = Folder(name = i,owner = self.user,permission = int_permission,parent_path = self.current.path)
                self.current.addFolder(_dir)
        
            print("owner : ",_dir.owner)
            print("permission : ",_dir.permission)

    def rm(self,inputData):
        if inputData.option is None:
            for i in inputData.args:
                match_obj = None

                for j in self.current.child_list:
                    if i == j.name:
                        match_obj = j
                    
                if match_obj is None:
                    print("there is no file")
                    continue
                    # raise ValueError
                
                if isFile(match_obj):
                    self.current.deleteFile(match_obj)
                elif isDir(match_obj):
                    print("it isn't file, it is dir")
                    #raise ValueError

        elif inputData.option == "-rf":
            for i in inputData.args:
                match_obj = None

                for j in self.current.child_list:
                    if i == j.name:
                        match_obj = j
                    
                if match_obj is None:
                    print("there is no file")
                    continue
                    # raise ValueError
                
                self.current.deleteFile(match_obj)

    def cp(self,inputData):

        if inputData.option is not None:
            #에러 만들어라(07/14)
            print("option is wrong")
            raise ValueError

        if not len(inputData.args) == 2:
            #에러 만들어라 (07/14)
            print("args is empty or it have just one arg")
            raise ValueError

        copied_file = inputData.args[0]
        copy_path = inputData.args[1]

        match_obj = None
        for child in self.current.child_list:
            if copied_file == child.name:
                match_obj = child

        if match_obj is None:
            print("there is no such file")
            raise ValueError

        if isDir(match_obj):
            print("it is dir")
            raise ValueError

        if self.current == self.root:
            temp_path = "/"
        else :
            temp_path = self.current.path

        path_list = dividePath(copy_path)
        safe_path = getSafePathFromPath(self.root,path_list)
        print("safe_path : ",safe_path)
        print("type(safe_path) : ",type(safe_path))

        copy_file_name = copy_path.replace(safe_path,"")

        if copy_file_name == "":
            copy_file_name = match_obj.name
        elif copy_file_name[0] == "/":
            copy_file_name = copy_file_name[1:]

        try:
            self.cd(InputData(["cd",safe_path]))
        except NoSuchDirectoryError:
            pass

        print("copy_file_name : ",copy_file_name)

        _file= File(name = copy_file_name,
                    owner = match_obj.owner,
                    permission = match_obj.permission,
                    parent_path = self.current.path,
                    content = match_obj.content)
        
        self.current.addFolder(_file)
        print("successfully done")
        self.cd(InputData(["cd",temp_path]))


    def cat(self,inputData):
        print(inputData.option)
        print(inputData.args)

        if inputData.option == ">":
            print("in > option")
            # 여러 인지가 입력된 경우 사용자 지정 에러 필(07/09)
            if len(inputData.args) > 1:
                print("so much filename")
                raise ValueError

            for i in self.current.child_list:
                # 똑같은 파일이나 디렉토리가 있는경우 사용자 에러 필(07/09)
                # 그럼 덮어쓰기가 불가능 -> 다른 방안을 생각해보자. (07/09)
                if inputData.args[0] == i.name:
                    print("there is same name file or directory")
                    raise ValueError
            
            con = str()

            try:
                while True:
                    con = con + input() + "\n"

            except EOFError as e:
                print("ctrl + d")

            print(con)

            _file = File(inputData.args[0],self.user,755,self.current.path,con)
            self.current.addFolder(_file)

        elif inputData.option == "-n":
            print("in -n option")
            #무조건 마지막에 \n이 입력되어 있는 에러 (07/10)

            for i in self.current.child_list:
                if inputData.args[0] == i.name:
                    match_obj = i

            #파일이 없는 경우 사용자 지정 에러 필(07/09)
            if match_obj is None:
                print("there is no file")
                raise ValueError

            if isFile(match_obj):
                str_list = match_obj.content.split("\n")
                print(str_list)

                index = 0
                for word in str_list:
                    index = index + 1
                    print(str(index)+"."+word)
                
            else:
                #파일이 아닌 경우 사용자 지정 에러 필(07/09)
                print("it is not file!")
                raise ValueError

        elif inputData.option is None:
            print("in non option")
            match_obj = None

            for i in self.current.child_list:
                if inputData.args[0] == i.name:
                    match_obj = i

            #파일이 없는 경우 사용자 지정 에러 필(07/09)
            if match_obj is None:
                print("there is no file")
                raise ValueError

            if isFile(match_obj):
                print(match_obj.name)
                print(match_obj.content)
            else:
                #파일이 아닌 경우 사용자 지정 에러 필(07/09)
                print("it is not file!")
                raise ValueError

    def find(self,inputData):

        if not inputData.option == "-name":
            #option이 잘못된 경우 사용자 지정 에러 필(07/11)
            print("option is wrong")
            raise ValueError

        if not len(inputData.args) == 2:
            #args이 잘못된 경우 사용자 지정 에러 필(07/11)
            print("args is empty or it have just one arg")
            raise ValueError

        #isPath가 필요없지 않을까?(07/12)
        path = inputData.args[0]
        find_name = inputData.args[1]

        if self.current == self.root:
            temp_path = "/"
        else :
            temp_path = self.current.path

        self.cd(InputData(["cd",path]))

        finalRecursiveFind(self.current,find_name)

        self.cd(InputData(["cd",temp_path]))

def recursiveFind(directory,find_name):
    for child in directory.child_list:
        if find_name == child.name:
            print("child.path : ",child.path)
    
    for child in directory.child_list:
        recursiveFind(child,find_name)

def _recursiveFind_(directory,find_name):
    for child in directory.child_list:
        if find_name in child.name:
            print("child.path : ",child.path)
    
    for child in directory.child_list:
        _recursiveFind_(child,find_name)

def _recursiveFind(directory,find_name):
    for child in directory.child_list:
        if child.name.endswith(find_name):
            print("child.path : ",child.path)
    
    for child in directory.child_list:
        _recursiveFind(child,find_name)

def recursiveFind_(directory,find_name):
    for child in directory.child_list:
        if child.name.startswith(find_name):
            print("child.path : ",child.path)
    
    for child in directory.child_list:
        recursiveFind_(child,find_name)

def finalRecursiveFind(directory,find_name):
    
    if "*" in find_name:
        re_name = find_name.replace("*","")
        if find_name[0] == "*" and find_name.endswith("*") and find_name.count("*") == 2:
            _recursiveFind_(directory,re_name)
        elif find_name[0] == "*" and find_name.count("*") == 1:
            _recursiveFind(directory,re_name)
        elif find_name.endswith("*") and find_name.count("*") == 1:
            recursiveFind_(directory,re_name)
        else:
            raise ValueError
    else:
        recursiveFind(directory,find_name)




        
