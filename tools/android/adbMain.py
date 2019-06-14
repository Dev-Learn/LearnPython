import sys
import os
import time
import subprocess
from functools import partial
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot, QThread
from PyQt5.QtCore import Qt
from tools.android.ui.ui_main_connect_adb import Ui_MainWindow

from tools.android.adbWorker import WorkerCheckAdb
from tools.android.adbDialog import AdbDeviceDialog

sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

SCAN_TIME = 5
deviceConnect = []


class AdbMain(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(AdbMain, self).__init__()
        self.setupUi(self)

        self.deviceDialog = []

        self.hasDevice()

        obj = WorkerCheckAdb()
        thread = QThread(self)
        obj.addDeviceConnect.connect(self.addDeviceConnect)
        obj.removeDeviceConnect.connect(self.removeDeviceConnect)
        obj.moveToThread(thread)
        thread.started.connect(partial(obj.runCheck))
        thread.start()

    @pyqtSlot(str, str)
    def addDeviceConnect(self, deviceName, deviceCode):
        deviceInfo = "%s - %s" % (deviceName, deviceCode)
        print("addDeviceConnect %s" % (deviceInfo))
        item = QtWidgets.QListWidgetItem()
        item.setData(Qt.UserRole, deviceCode)
        item.setText(deviceInfo)
        self.listDevice.addItem(item)
        self.hasDevice()

        # subprocess.call("""adb -s %s exec-out screenrecord --bit-rate=16m --output-format=h264 --size 1920x1080  | /Applications/vlc.app/Contents/MacOS/VLC --demux h264""" % deviceCode)
        dialog = AdbDeviceDialog(deviceInfo=deviceInfo, deviceCode=deviceCode)
        self.deviceDialog.append(dialog)
        dialog.show()
        if dialog.exec_() == QtWidgets.QDialog.Rejected:
            print("CLEAR - THREAD")
            dialog.clear()

    @pyqtSlot(str)
    def removeDeviceConnect(self, deviceCode):
        print("removeDeviceConnect %s" % deviceCode)
        for index in range(self.listDevice.count()):
            item = self.listDevice.item(index)
            data = item.data(Qt.UserRole)
            if deviceCode in data:
                self.listDevice.takeItem(self.listDevice.row(item))
        #         adb shell "while true; do screenrecord --bit-rate=16m --output-format=h264 --size 1920x1080 -; done" | ffplay -
        # adb -s CB512ETBS9 shell "while true; do screenrecord --output-format=h264 --time-limit 1 -; done" | /Applications/vlc.app/Contents/MacOS/VLC --demux h264 -

        for dialog in self.deviceDialog:
            if dialog.checkCode(deviceCode):
                print("CLEAR - THREAD")
                dialog.clear()
                dialog.close()

        self.hasDevice()

    def hasDevice(self):
        if self.listDevice.__len__() == 0:
            self.lableNoDevice.setVisible(True)
            self.listDevice.setVisible(False)
        else:
            self.lableNoDevice.setVisible(False)
            self.listDevice.setVisible(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = AdbMain()
    main.raise_()
    main.show()
    sys.exit(app.exec())
