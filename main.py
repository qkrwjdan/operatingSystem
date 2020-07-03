# 본 프로젝트에서 구현하는 내용은 다음과 같다.
# - 리눅스 시스템과 동일한 파일 탐색기 구조를 구현한다.
# - 필수 구현 명령어 : cd, mkdir, pwd, ls, rm, cat, cp, find
# - 명령어 별 수업 시간에 설명한 옵션들 구현
# - cat 명령어를 통해서 파일 생성 및 읽기 구현
# - 파일 입출력을 통해서 폴더 및 파일 생성된 현황을 저장하고 읽어야 함
# - mkdir 명령어를 통해서 다수의 폴더를 동시에 생성할 수 있어야 함
# - 위 명령어 이외의 명령어 구현 시 추가 점수 (최대 3개)
# - mkdir 명령어에서 다수의 폴더 생성 시 멀티스레딩을 이용하여 동시에 생성할 것 - 이 외의 명령어에서도 동시 작업 발생 시 멀티스레딩 적용
# (어느 작업에서 동시 작업이 발생하는지 잘 생각해 볼 것)


"""
-pwd 
현재 작업중인 디렉토리의 절대경로 출력.

-cd
디렉토리를 이동 가능.

*옵션
1.cd directoryName -> directoryName 으로 이동
2.cd / -> 루트(/)디렉토리로 이동
3.cd 절대경로 -> 절대경로로 이동
4.cd . -> 현재 디렉토리로 이동
5.cd .. -> 상위 디렉토리로 이동
6.cd ~ -> 자신의 홈 디렉토리로 이동
7.cd - -> 이전 경로로 이동

**구현옵션 : 
1.cd . 
2.cd .. 
3.cd ~ 
4.cd 절대경로 
5.cd 상대경로

-mkdir
디렉토리를 만든다.

*옵션
1.mkdir 파일이름 -> 파일이름의 디렉토리를 만든다.
2.mkdir 파일이름 파일이름 파일이름 -> 여러 파일 한번에 생성가능, 멀티스레딩을 이용하여 동시에 생성
3.mkdir -m 권한 파일이름 -> 디렉토리를 생성할 때 권한을 설정한다. default = 777
4.mkdir -p 파일경로 -> 절대경로, 상대경로 가능, 파일경로에 디렉토리를 생성한다.

**구현옵션 
1. mkdir dir1 dir2 dir3...
2. mkdir –p dir1/dir2/dir3...
3. mkdir –m 3-digits filename


-ls
현재 디렉토리의 파일에 대한 리스트를 보여준다.

*옵션
1.ls -a -> 숨겨진 파일이나 디렉토리도 보여준다.
2.ls -d -> 디렉토리만 보여준다.
3.ls -l -> 각 파일의 모드,링크수,소유자,그룹,크기,최종수정시간을 표시한다.
4.ls -m -> 쉼표로 구분
5.ls -r -> 역순으로 표시
6.ls -R -> 하위의 서브 디렉토리 내용도 표시
7.ls -t -> 시간순으로 표시
8.ls -s -> 크기순으로 표시

**구현옵션 : a,l,al,ll

-rm
파일을 삭제한다.

*옵션
1.rm 파일이름 -> 파일이름의 파일을 삭제한다.
2.rm *.dat -> 확장자가 .dat인 파일을 삭제한다.
3.rm * -> 모든 파일을 삭제한다.
4.rm -r 디렉토리이름 -> 디렉토리를 삭제한다.
5.rm -rf 디렉토리이름 -> 경고없이 디렉토리를 삭제한다.
6.rm -ri 디렉토리이름 -> 하나하나 확인하면서 삭제한다.

**구현옵션 : rf

-cat
파일의 내용을 출력한다.

*옵션
1.cat filename1 filename2 filename3 -> 여러 파일들을 출력한다.
2.cat file1 file2 > file3 -> file1과 file2를 합쳐 file3을 만든다. file3이 존재하는 파일이면 그 위에 덮어쓴다.
3.car file1 >> file2 -> file2의 끝에 file1의 내용을 덧붙여준다.
4.car > newfile -> 새로운 파일을 생성한다. 이 명령 후에 표준 입력으로 키보드에서 입력한 내용을 파일에 저장된다. ctrl + d -> 파일 저장
5.-b: 줄번호를 화면 왼쪽에 나타낸다. 비어있는 행은 제외한다.
6.-e: 제어 문자를 ^ 형태로 출력하면서 각 행의 끝에 $를 추가한다.
7.-n: 줄번호를 화면 왼쪽에 나타낸다. 비어있는 행도 포함한다.
8.-s: 연속되는 2개이상의 빈 행을 한행으로 출력한다.
9.-v: tab과 행 바꿈 문자를 제외한 제어 문자를 ^ 형태로 출력한다.
10.-E: 행마다 끝에 $ 문자를 출력한다.
11.-T: 탭(tab) 문자를 출력한다.
12.-A: -vET 옵션을 사용한 것과 같은 효과를 본다.

**구현옵션 : cat > filename / cat filename / cat -n name

-cp
파일이나 디렉토리를 복사한다.

*옵션
1.-b : 복사하고자 하는 파일이 동일한 이름으로 이미 그 위치에 존재하고 있을 경우, 덮어쓰기 또는 원본을 지우고 복사할 경우에 원본파일의 복사본을 만든다.
2.-f : 복사대상파일이 이미 그 위치에 존재한다면 파일을 지우고 복사한다.
3.-i : 복사대상파일이 이미 그 위치에 존재한다면 덮어쓸 것인가를 사용자에게 확인, 기본으로 앨리어싱되어 있음.
4.-P : 복사대상이 되는 원본파일이 디렉토리경로와 함게 지정되었을 경우에 지정된 디렉토리경로를 그대로 복사한다. 즉 이 경우 원본파일은 dir1/subdir2/filename 등과 같이 디렉토리경로와 함께 지정되어야 한다.
5.-u(--update) : 복사되는 원본파일의 이름과 동일한 파일이 대상위치에 존재할 경우에 원본파일과 변경날짜를 비교하여 최신파일일 경우에 복사하지 않는 옵션이다. 즉 원본파일이 목적파일 보다 최신 파일일 경우에만 복사하는 옵션이다.
6.-r 또는 -R (--recursive) : 복사대상이 하위디렉토리와 파일들을 가지고 있을때 모두 동일하게 복사하는 옵션이다.
9.-p : 복사되어 새로 생성되는 파일이 원본파일과 동일한 모드, 소유자, 시간정보를 가지도록 하는 옵션이다.

**구현옵션 : cp file1 newfile / cp file1 절대경로/dir1 / cp file1 절대경로/dir1/newfile

-find
파일 및 디렉토리를 찾는다.

*옵션
1. find 상대경로/절대경로 (-name) (*part)
2. find 상대경로/절대경로 (-name) (part*)
3. find 상대경로/절대경로 (-name) (*part*)
4. find 상대경로/절대경로 (-name) (part)

"""
from input import inputData
from objects import File,Folder,User,ObjectHandler
from userExceptions import *

def initProgram():
    user = User("park","1234")
    root = Folder("root",0,)
    user_folder = Folder(user.name,0,root.name)
    root.addFolder(user_folder)

    handler = ObjectHandler(root,user)
    return handler

if __name__ == "__main__":

    handler = initProgram()

    while(True):
        print("{user}:{current} macbookair$ ".format(user = handler.user.name,current = handler.current.name),end="")

        print("current path : ",handler.current.path)
        avg = input()

        if(avg == "exit"):
            break

        inputList = avg.split(" ")

        try:
            dat = inputData(inputList)
        except NoDataError as e:
            continue
        except CommandError as e:
            print(e,"{command} is wrong".format(command = inputList[0]))
            continue
        

        # print(dat)

        if dat.command == "cd":
            try:
                handler.cd(dat)
            except ValueError as e:
                print(e)
                pass
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


