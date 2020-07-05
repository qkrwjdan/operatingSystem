import time
from sys import getsizeof

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
        self.size = getsizeof(self)
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


if __name__ == "__main__":
    u1 = User("park","pwd")
    f1 = Folder("park",0,u1,755,"root")

    print(f1.size)
    print(type(f1.size))

    f2 = Folder("park",0,u1,755,"root")
    f3 = Folder("park",0,u1,755,"root")

    f1.addFolder(f2)
    f1.addFolder(f3)

    print(f1.size)
    print(type(f1.size))

    print(getsizeof(f1))



        
