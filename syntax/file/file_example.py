
# encoding : https://www.youtube.com/watch?v=MwqDZb0QEl0&index=18&list=PLUujJDuOx6BIsByGjnCAum1do3erXsl81

file_name = 'test.txt'

def create_file() :
    f = open(file_name,mode='w')
    for x in range(1,21):
        f.write(str(x) + '\n')
    f.close()

def open_file():
    try:
        f = open(file_name,mode='r')
        t = f.read()
        print(t)
    except FileNotFoundError :
        print('Ko tìm thấy file :  %s' % file_name )
    finally:
        f.close()

create_file()
open_file()
