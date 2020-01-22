import sys
import os
import time
import subprocess
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class WorkerCheckAdb(QObject):
    addDeviceConnect = pyqtSignal(str, str)
    removeDeviceConnect = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.deviceConnect = []

    def setUpConnect(self, deviceCode):
        deviceName = subprocess.Popen("adb -s %s shell getprop ro.product.brand" % deviceCode, shell=True,
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        deviceName = deviceName.stdout.read().strip()
        deviceName = str(deviceName.strip()).strip().split("'")[1]
        # print("setUpConnect %s - %s" % (deviceName, deviceCode))
        self.addDeviceConnect.emit(deviceName, deviceCode)

    def removeConnect(self, deviceCode):
        self.removeDeviceConnect.emit(deviceCode)

    def isNotConnect(self, device):
        isNotConnect = device["isConnect"] == False
        if isNotConnect:
            self.removeConnect(device["code"])
        return isNotConnect

    @pyqtSlot()
    def runCheck(self):
        while True:
            for device in self.deviceConnect:
                device["isConnect"] = False

            result = os.popen("adb devices").read()
            # print(result)
            result = result.split("\n")
            for item in result:
                if "\tdevice" in item:
                    deviceCode = item.split("\tdevice")[0]
                    device = {"code": deviceCode, "isConnect": False}
                    if device not in self.deviceConnect:
                        self.deviceConnect.append({"code": deviceCode, "isConnect": True})
                        self.setUpConnect(deviceCode)
                    else:
                        index = self.deviceConnect.index(device)
                        device = self.deviceConnect[index]
                        device["isConnect"] = True

            self.deviceConnect[:] = [device for device in self.deviceConnect if not self.isNotConnect(device)]

            # print(self.deviceConnect)
            time.sleep(5)
