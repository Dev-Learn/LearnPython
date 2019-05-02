import subprocess
from time import sleep
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
    ips = "164.77.124.195".split(".")
    port = "59058"
    subprocess.call("adb shell am start -n com.android.settings/com.android.settings.wifi.WifiSettings", shell=True)
    sleep(0.5)
    subprocess.call("adb shell input swipe 350 600 350 600 500", shell=True)
    sleep(0.5)
    subprocess.call("adb shell input tap 625 900", shell=True)
    subprocess.call("adb shell input keyevent KEYCODE_BACK", shell=True)
    subprocess.call("adb shell input tap 500 1125", shell=True)
    subprocess.call("adb shell input tap 500 1065", shell=True)
    subprocess.call("adb shell input tap 500 1200", shell=True)
    subprocess.call("adb shell input tap 800 1325", shell=True)
    sleep(0.1)
    subprocess.call("adb shell input keyevent KEYCODE_MOVE_END", shell=True)
    subprocess.call("adb shell input keyevent --longpress $(printf 'KEYCODE_DEL %.0s' {1..250})", shell=True)
    sleep(0.1)

    for index,ip in enumerate(ips):
        subprocess.call("adb shell input text " + ip, shell=True)
        if index != ips.__len__() - 1:
            subprocess.call("adb shell input text .", shell=True)

    subprocess.call("adb shell input keyevent KEYCODE_BACK", shell=True)
    sleep(0.1)
    subprocess.call("adb shell input tap 800 1000", shell=True)
    sleep(0.1)
    subprocess.call("adb shell input keyevent KEYCODE_MOVE_END", shell=True)
    subprocess.call("adb shell input keyevent --longpress $(printf 'KEYCODE_DEL %.0s' {1..250})", shell=True)
    sleep(0.1)
    subprocess.call("adb shell input text " + port, shell=True)
    sleep(0.1)
    subprocess.call("adb shell input keyevent KEYCODE_BACK", shell=True)
    subprocess.call("adb shell input tap 850 1650", shell=True)
    subprocess.call("adb shell input keyevent KEYCODE_HOME", shell=True)
    subprocess.call("adb shell input tap 750 1650", shell=True)
    subprocess.call("adb shell input tap 500 150", shell=True)
    subprocess.call("adb shell input keyevent KEYCODE_ENTER", shell=True)

