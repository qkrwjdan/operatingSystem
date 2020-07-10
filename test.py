from objects import File,Folder,Object,User

if __name__ == "__main__":
    

    _list = [1,2,3,4,5,1,2,3,4,5]

    index = 0
    for ele in _list:
        print("ele : ",ele,"index : ",index)
        index = index + 1

    index = 0
    for ele in _list:
        if ele == 3:
            del _list[index]
            break
        index = index + 1
    
    print(_list)


    

