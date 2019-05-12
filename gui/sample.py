import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)

due = input("Enter Time for Alert (format : hh:mm) : ")
message = input("Enter Message for Alert : ")

try:
    hours, mins = due.split(":")
    due = QTime(int(hours), int(mins))
    if not due.isValid():
        raise ValueError
except ValueError:
    message = "Time entered is not valid time"

while QTime.currentTime() < due:
    time.sleep(20)

label = QLabel("<font color=red size 200><b>" + message + "</b></font>")
label.setWindowFlag(Qt.SplashScreen)
label.show()
QTimer.singleShot(60000, app.quit)
sys.exit(app.exec_())
