from objects import File,Folder,isDir,isFile

if __name__ == "__main__":
    while(True):
        _dir = Folder(name = "i",size = 0,owner = "user",permission = 755,parent_path = "path")

        print(_dir.name)
        print(_dir.size)
        print(_dir.owner)
        print(_dir.permission)
        print(_dir.path)
        print(_dir.name)

