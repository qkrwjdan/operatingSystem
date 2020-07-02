from userExceptions import *

class inputData:

    def __init__(self,args):

        self.command = None
        self.option = None
        self.args = list()
        self.argLen = len(args)

        if args[0] == "":
            raise NoDataError

        if args[0] in ["cd","ls","pwd","mkdir","rm","cat","cp","find"]:
            self.command = args[0]
        else:
            raise CommandError

        for argument in args[1:]:
            try :
                if argument[0] == "-" or argument[0] == ">":
                    self.option = argument
                else:
                    self.args.append(argument)
            except IndexError as e:
                print("argument : ",argument," is wrong arg")
                print(e)

    def __str__(self):
        print("==============")
        print("command : ",self.command)
        print("option : ",self.option)
        print("argLen : ",self.argLen)
        for i in self.args:
            print(i)
        
        return super.__str__(self)

if __name__ == "__main__":
    print(type("string"))
    while(True):
        print("User:directoryName macbookair$ ",end="")
        avg = input()

        if(avg == "exit"):
            break

        aList = avg.split(" ")

        dat = inputData(aList)


        

