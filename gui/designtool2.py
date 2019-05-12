import json
import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import *

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app = QApplication(sys.argv)
dlg = uic.loadUi("test2.ui")
data = []


def addItem(file):
    print(file)
    text = dlg.lineEdit.text()
    if "" != text:
        print(dlg.lineEdit.text())
        dlg.listWidget.addItem(text)
        dlg.lineEdit.setText("")
        dlg.lineEdit.setFocus(True)
    else:
        show_message("Warning", "You have to type at least one element")
    data.append(text)
    try:
        with open(file.name, "w") as fileData:
            json.dump(data, fileData)
    except Exception as e:
        print(e)


def show_message(title, message):
    QMessageBox.information(None, title, message)


def main():
    file = os.path.join(APP_ROOT, 'data.json')
    print(file)

    if not os.path.isfile(file):
        file = open(file, 'w')
    else:
        file = open(file, 'r')

    try:
        data = json.load(file)
        print(data)
        for item in data :
            dlg.listWidget.addItem(item)
    except Exception as e:
        print(e)

    dlg.lineEdit.setFocus(True)
    dlg.pushButton.clicked.connect(lambda: addItem(file))
    dlg.lineEdit.returnPressed.connect(lambda: addItem(file))

    dlg.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
