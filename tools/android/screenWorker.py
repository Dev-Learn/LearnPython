import subprocess
import cv2, os,time
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class WorkerScreenCap(QObject):
    pathImage = pyqtSignal(str)

    def __init__(self,deviceCode):
        super().__init__()
        self.deviceCode = deviceCode

    def runScreenCap(self):
        dir = 'screencap'

        if not os.path.isdir(dir):
            os.mkdir(dir)
        while True:
            subprocess.call("adb -s %s shell screencap /sdcard/%s_screen.png" % (self.deviceCode, self.deviceCode), shell=True)
            subprocess.call("adb -s %s pull /sdcard/%s_screen.png %s" % (self.deviceCode, self.deviceCode, os.path.abspath(dir)),
                            shell=True)
            self.pathImage.emit(os.path.join(dir, "%s_screen.png" % self.deviceCode))
            # time.sleep(1)
