import subprocess
import cv2, os, time
from array import array
import numpy as np
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
        adbCmd = ['adb', 'exec-out', 'screenrecord', '--size', '450x800', '--output-format=h264', '-']
        stream = subprocess.Popen(adbCmd, stdout=subprocess.PIPE)

        ffmpegCmd = ['ffmpeg', '-i', '-', '-f', 'rawvideo', '-s', '800x450',
                     '-vcodec', 'bmp', '-']
        ffmpeg = subprocess.Popen(ffmpegCmd, stdin=stream.stdout, stdout=subprocess.PIPE)

        # while True:
        #     fileSizeBytes = ffmpeg.stdout.read(6)
        #     print(fileSizeBytes)
        #     fileSize = 0
        #     for i in range(4):
        #         fileSize += array('B', fileSizeBytes[i + 2])[0] * 256 ** i
        #     bmpData = fileSizeBytes + ffmpeg.stdout.read(fileSize - 6)
        #     print(bmpData)
        #     image = cv2.imdecode(np.fromstring(bmpData, dtype=np.uint8), 1)
        #     cv2.imshow("im", image)
        #     cv2.waitKey(25)

        while True:
            raw_image = ffmpeg.stdout.read(800 * 450 * 3)
            # print(raw_image)
            image = np.frombuffer(raw_image, np.uint8)
            image = image.reshape((800, 450, 3))
            cv2.imshow('', image)
            cv2.waitKey()
            # img.loadFromData(raw_image)
            # self.image.emit(img)
            # print(raw_image)
            # image = numpy.fromstring(raw_image, dtype='uint8')
            # image = image.reshape((324, 576, 3))
            # image = cv2.imdecode(image, 1)
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
