import subprocess

from pip._vendor.distlib.compat import raw_input

# https://stackoverflow.com/questions/2604727/how-can-i-connect-to-android-with-adb-over-tcp
def connect():
    print("Input command : \n")
    while True:
        input = raw_input()
        if input == 'exit':
            break
        subprocess.call(input, shell=True)


if __name__ == '__main__':
    connect()