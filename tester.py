from input import InputData
from objects import File,Folder,User,ObjectHandler
from userExceptions import *
from main import initProgram

if __name__ == "__main__":

    test_list = list()
    test_list.append("mkdir -p /a/b/c")
    test_list.append("cd /a/b")
    test_list.append("mkdir -p /a/b/c/d")
    test_list.append("pwd")
    
    for avg in test_list:
        print("test avg : ",avg)

        handler = initProgram()

        inputList = avg.split(" ")

        try:
            dat = InputData(inputList)
        except NoDataError as e:
            print(e)
        except CommandError as e:
            print(e,"{command} is wrong".format(command = inputList[0]))

        if dat.command == "cd":
            try:
                handler.cd(dat)
            except NoSuchDirectoryError:
                pass
            except ValueError as e:
                print(e)

        elif dat.command == "pwd":
            handler.pwd(dat)
        elif dat.command == "ls":
            handler.ls(dat)
        elif dat.command == "mkdir":
            try:
                handler.mkdir(dat)
            except FileOrFolderNameError as e:
                print(e)

        elif dat.command == "cp":
            handler.cp(dat)
        elif dat.command == "cat":
            handler.cat(dat)
        elif dat.command == "rm":
            handler.rm(dat)
        elif dat.command == "find":
            handler.find(dat)


