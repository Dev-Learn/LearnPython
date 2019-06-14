from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QThread,Qt
from PyQt5.QtGui import QPixmap,QImage
from functools import partial
from tools.android.ui.ui_adb_device import Ui_Dialog
from tools.android.screenWorker import WorkerScreenCap


class AdbDeviceDialog(Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, deviceInfo=None, deviceCode=None, parent=None):
        super(AdbDeviceDialog, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle(deviceInfo)
        self.setObjectName(deviceCode)
        self.image = QImage()
        self.imageShow.resize(450, 800)

        self.obj = WorkerScreenCap(deviceCode)
        self.thread = QThread(self)
        self.obj.image.connect(self.pathImageScreenCap)
        self.obj.moveToThread(self.thread)
        self.thread.started.connect(partial(self.obj.runScreenCap))
        self.thread.start()

    def clear(self):
        print("CLEAR - THREAD")
        self.obj.readData = False
        self.thread.exit()

    def checkCode(self, code):
        return code == self.objectName()

    @pyqtSlot(QImage)
    def pathImageScreenCap(self, img):
        # pixmap = QPixmap(path)
        # self.image = QPixmap.toImage(img)
        if img:
            image = img.scaled(450, 800, Qt.KeepAspectRatio)
            self.imageShow.setPixmap(QPixmap.fromImage(image))

    if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        dialog = AdbDeviceDialog()
        dialog.show()
        app.exec_()
