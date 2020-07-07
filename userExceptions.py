class FileOrFolderNameError(Exception):

    def __init__(self,info = ""):
        super().__init__("syntax error : name is wrong \n",info)

class NoDataError(Exception):

    def __init__(self):
        super().__init__("no data")

class CommandError(Exception):

    def __init__(self,info = ""):
        super().__init__("syntax error : command \n",info)

class NoSuchDirectoryError(Exception):

    def __init__(self,info = ""):
        super().__init__("there is no such dir \n",info)