import sys

from PyQt5.QtWidgets import *


class Form(QDialog):
    def __init__(self):
        super().__init__()

        self.brower = QTextBrowser()
        self.line_edit = QLineEdit("Type an expression and press Enter")
        self.line_edit.selectAll()
        layout = QVBoxLayout()
        layout.addWidget(self.brower)
        layout.addWidget(self.line_edit)
        self.setLayout(layout)
        self.line_edit.setFocus()
        self.line_edit.returnPressed.connect(self.updateUI)
        self.setWindowTitle("Calculator")

    def updateUI(self):
        try:
            text = self.line_edit.text()
            self.brower.append("%s = <b>%s</b>" % (text,eval(text)))
            self.line_edit.clear()
        except Exception:
            self.brower.append("<b>%s is invalid</b>")


app = QApplication(sys.argv)
form = Form()
form.show()
sys.exit(app.exec_())
