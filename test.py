from objects import File,Folder,Object,User

if __name__ == "__main__":
    
    _str = "asd\nlajsf\nkjal;sgd\nlkajsd\nlkajsgd\n"

    print(_str)
    _list = _str.split("\n")
    print(_list)

    index = 0
    for word in _list:
        index = index + 1
        print(str(index)+"."+word)

    

