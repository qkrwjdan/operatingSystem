from objects import File,Folder,Object,User

def intToPermissionString(one_digit):
    if one_digit == 7:
        print("wrx")
        return "wrx"
    elif one_digit == 6:
        print("wr-")
        return "wr-"
    elif one_digit == 5:
        print("w-x")
        return "w-x"
    elif one_digit == 4:
        print("w--")
        return "w--"
    elif one_digit == 3:
        print("-rx")
        return "-rx"
    elif one_digit == 2:
        print("-r-")
        return "-r-"
    elif one_digit == 1:
        print("--x")
        return "--x"

def getPermissionStr(permission):
    owner_permission = int(permission / 100)
    group_permission = int(permission / 10) % 10
    etc_permission = permission % 10

    permission_str = intToPermissionString(owner_permission) + intToPermissionString(group_permission) + intToPermissionString(etc_permission)
    return permission_str

if __name__ == "__main__":
    print(getPermissionStr(755))
    

