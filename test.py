from objects import File,Folder,Object,User

if __name__ == "__main__":
    
    content = str()
    while True:
        try:
            while True:
                content = content + input() + "\n"

        except EOFError as e:
            print("error")
            print(e)
            break
        
        if content == "exit":
            break
    
    
    print(content)


    

