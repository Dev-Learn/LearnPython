import subprocess
import cv2, os,time
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class WorkerScreenCap(QObject):
    pathImage = pyqtSignal(str)

    def __init__(self,deviceCode):
        super().__init__()
        self.deviceCode = deviceCode
        self.readData = True

    def runScreenCap(self):
        print("run ScreenCap")
        dir = 'screencap'

        if not os.path.isdir(dir):
            os.mkdir(dir)
        data = subprocess.Popen("adb -s %s exec-out screenrecord --bit-rate=16m --output-format=h264 --size 1920x1080 -" % self.deviceCode, shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while self.readData:
            line = data.stdout.readline()
            print(line)
