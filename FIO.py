import pickle

class testObj:
    
    def __init__(self):
        self.a = 10
        self.b = 100

if __name__ == "__main__":
    obj1 = testObj()

    with open("test.bin","a+b") as file:
        pickle.dump(obj1,file)

    with open("test.bin","r+b") as file:
        readObj1 = pickle.load(file)

    print(obj1.a)
    print(readObj1.a)

