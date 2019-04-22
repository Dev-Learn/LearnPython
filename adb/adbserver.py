import subprocess
from time import sleep

from uiautomator import Device
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
    # connect()
    subprocess.call("adb shell input keyevent 26 82", shell=True)
    sleep(1)
    subprocess.call("adb shell input tap 545 1656", shell=True)
    sleep(1)
    subprocess.call("adb shell input swipe 550 500 500 500 100", shell=True)
    sleep(0.5)
    subprocess.call("adb shell input swipe 550 500 500 500 100", shell=True)
    sleep(0.5)
    subprocess.call("adb shell input tap 925 670", shell=True)
    sleep(1)
    subprocess.call("adb shell input swipe 500 1300 500 300 100", shell=True)
    sleep(0.5)
    subprocess.call("adb shell input swipe 500 1300 500 300 100", shell=True)
    sleep(0.5)
    subprocess.call("adb shell input swipe 500 300 500 1300 100", shell=True)
    sleep(0.5)
    subprocess.call("adb shell input swipe 500 300 500 1300 100", shell=True)
    sleep(1)
    subprocess.call("adb shell input tap 250 300", shell=True)
    count = 0
    while True:
        count += 1
        if count < 10:
            sleep(0.5)
            subprocess.call("adb shell input swipe 750 500 500 500 100", shell=True)
        elif count < 15:
            subprocess.call("adb shell input swipe 500 500 750 500 100", shell=True)
        else:
            break
    subprocess.call("adb shell input keyevent 4", shell=True)
    sleep(0.5)
    subprocess.call("adb shell input keyevent 4", shell=True)
    sleep(0.5)
    subprocess.call("adb shell input keyevent KEYCODE_APP_SWITCH", shell=True)
    sleep(0.5)
    subprocess.call("adb shell input tap 900 200", shell=True)
    sleep(0.5)
    subprocess.call("adb shell input keyevent 26", shell=True)