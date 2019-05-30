import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class ResizeDlg(QDialog):
    def __init__(self, width, height, parent=None):
        super(ResizeDlg, self).__init__(parent)

        titleWidth = QLabel("Width:")
        self.widthSpinBox = QSpinBox()
        titleWidth.setBuddy(self.widthSpinBox)
        self.widthSpinBox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.widthSpinBox.setRange(4, width * 4)
        self.widthSpinBox.setValue(width)
        titleHeight = QLabel("&Height:")
        self.heightSpinBox = QSpinBox()
        titleHeight.setBuddy(self.heightSpinBox)
        self.heightSpinBox.setAlignment(Qt.AlignRight |
                                        Qt.AlignVCenter)
        self.heightSpinBox.setRange(4, height * 4)
        self.heightSpinBox.setValue(height)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok |
                                     QDialogButtonBox.Cancel)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout = QGridLayout()
        layout.addWidget(titleWidth, 0, 0)
        layout.addWidget(self.widthSpinBox, 0, 1)
        layout.addWidget(titleHeight, 1, 0)
        layout.addWidget(self.heightSpinBox, 1, 1)
        layout.addWidget(button_box, 2, 0, 1, 0)

        self.setLayout(layout)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        self.setWindowTitle("Image Changer - Resize")

    def result(self):
        return self.widthSpinBox.value(), self.heightSpinBox.value()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = ResizeDlg(100, 100)
    form.show()
    sys.exit(app.exec_())
