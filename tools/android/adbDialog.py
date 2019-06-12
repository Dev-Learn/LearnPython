from PyQt5 import QtWidgets
from tools.android.ui.ui_adb_device import Ui_Dialog


class AdbDeviceDialog(Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, deviceInfo = None, deviceCode = None, parent=None):
        super(AdbDeviceDialog, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle(deviceInfo)
        self.setObjectName(deviceCode)

    def checkCode(self,code):
        return code == self.objectName()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    dialog = AdbDeviceDialog()
    dialog.show()
    app.exec_()
