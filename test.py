from objects import File,Folder,isDir,isFile

if __name__ == "__main__":
    a = File("file",0,"root")
    b = Folder("folder",0,"root")

    print(type(b))
    if isDir(b):
        print("success!")

    if isFile(b):
        print("fail")

    print(type(a))
    if isDir(a):
        print("success!")

    if isFile(a):
        print("fail")