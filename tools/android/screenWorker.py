import subprocess
import cv2, os, time
from array import array
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5 import QtGui


class WorkerScreenCap(QObject):
    image = pyqtSignal(QtGui.QImage)

    def __init__(self, deviceCode):
        super().__init__()
        self.deviceCode = deviceCode
        self.readData = True

    def runScreenCap(self):
        print("run ScreenCap")
        dir = 'screencap'

        if not os.path.isdir(dir):
            os.mkdir(dir)
        img = QtGui.QImage()
        adbCmd = ['adb', '-s %s' % self.deviceCode, 'exec-out', 'screenrecord', '--output-format=h264', '-']
        # stream = subprocess.Popen(adbCmd, stdout=subprocess.PIPE)
        #
        # ffmpegCmd = ['ffmpeg', '-i', '-', '-f', 'rawvideo', '-vf', 'scale=324:576',
        #              '-vcodec', 'bmp', '-']

        # ffmpeg = subprocess.Popen(ffmpegCmd, stdin=stream.stdout, stdout=subprocess.PIPE)
        ffmpeg = subprocess.Popen("adb -s %s exec-out screenrecord --output-format=h264 - | ffmpeg -i --f rawvideo -vf scale=324:576 -vcodecbmp -" % self.deviceCode, shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        while True:
            fileSizeBytes = ffmpeg.stdout.read()
            print(fileSizeBytes)
            fileSize = 0
            try:
                for i in range(4):
                    fileSize += array('B', fileSizeBytes[i + 2])[0] * 256 ** i
                bmpData = fileSizeBytes + ffmpeg.stdout.read(fileSize - 6)
                img.loadFromData(bmpData)
                self.image.emit(img)
            except Exception as e:
                a = 1
                # print(e)
            # image = cv2.imdecode(np.fromstring(bmpData, dtype=np.uint8), 1)
            # cv2.imshow("im", image)
            # cv2.waitKey(25)



            # data = subprocess.Popen("adb -s %s exec-out screencap -p" % self.deviceCode, shell=True,
            #                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # img.loadFromData(data.stdout.read())
            # self.image.emit(img)
            # total = bytes()
            # while True:
            #     line = data.stdout.readline()
            #     total += line
            #     # print(total)
            #     if not line:
            #         print("Complete")
            #         break
            #     else:
            #         img.loadFromData(total)
            #         self.image.emit(img)
