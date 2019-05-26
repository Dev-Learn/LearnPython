import sys
from PyQt5.QtWidgets import *


class Form(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.dial = QDial()
        self.dial.setNotchesVisible(True)

        self.spinBox = QSpinBox()

        layout = QHBoxLayout()
        layout.addWidget(self.dial)
        layout.addWidget(self.spinBox)

        self.setLayout(layout)
        self.setWindowTitle("Signals and Slots")
        self.dial.valueChanged.connect(self.updateSpinner)
        self.spinBox.valueChanged.connect(self.updateDial)

    def updateSpinner(self):
        print(self.dial.value())
        self.spinBox.setValue(self.dial.value())

    def updateDial(self):
        print(self.spinBox.value())
        self.dial.setValue(self.spinBox.value())


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
