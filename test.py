from objects import File,Folder,isDir,isFile

if __name__ == "__main__":
    ps = "/"
    li = ps.split("/")
    li = ps[1:].split("/")

    ps2 = "a/b/c/d"
    li2 = ps2.split("/")
    li2.pop()
    

    ps3 = "/a/b/c/d"
    li3 = ps3.split("/")
    lis3 = li3[1:]

    ps4 = "/"
    li4 = ps4.split("/")


    print(li)
    print(li2)
    print(li3)
    print(li4)
    print(lis3)