from PyQt5 import QtWidgets, uic


def Convert():
    dlg.lineEdit_2.setText(str(float(dlg.lineEdit.text()) * 1.23))


app = QtWidgets.QApplication([])
dlg = uic.loadUi("test.ui")

dlg.lineEdit.setFocus()
dlg.lineEdit.setPlaceholderText("Euro")
dlg.lineEdit_2.setPlaceholderText("USD")
dlg.pushButton.clicked.connect(Convert)

dlg.lineEdit.returnPressed.connect(Convert)
dlg.lineEdit_2.setReadOnly(True)

dlg.show()
app.exec()
