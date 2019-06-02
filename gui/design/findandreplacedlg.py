import sys
import re

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import *
from PyQt5.uic.properties import QtGui

from gui.design import ui_findandreplacedlg

MAC = hasattr(QtGui, "qt_mac_set_native_menubar")

# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

from PyQt5.QtCore import pyqtSlot

class FindAndReplaceDlg(QDialog, ui_findandreplacedlg.Ui_FindAndReplaceDlg):

    def __init__(self, text, parent=None):
        super(FindAndReplaceDlg, self).__init__(parent)
        self.__text = text
        self.__index = 0
        self.setupUi(self)
        if not MAC:
            self.findButton.setFocusPolicy(Qt.NoFocus)
            self.replaceButton.setFocusPolicy(Qt.NoFocus)
            self.replaceAllButton.setFocusPolicy(Qt.NoFocus)
            self.closeButton.setFocusPolicy(Qt.NoFocus)
        self.updateUi()

    def text(self):
        return self.__text

    @pyqtSlot("QString")
    def on_findLineEdit_textEdited(self):
        self.__index = 0
        self.updateUi()

    def updateUi(self):
        enable = self.findLineEdit.text() != ""
        self.findButton.setEnabled(enable)
        self.replaceButton.setEnabled(enable)
        self.replaceAllButton.setEnabled(enable)

    @pyqtSlot()
    def on_findButton_clicked(self):
        print("on_findButton_clicked")
        regex = self.makeRegex()
        print(regex)
        match = regex.search(self.__text, self.__index)
        if match is not None:
            self.__index = match.end()
            print("Found at %d" % match.start())
        else:
            print("No more found")

    @pyqtSlot()
    def on_replaceButton_clicked(self):
        regex = self.makeRegex()
        self.__text = regex.sub(self.replaceLineEdit.text(), self.__text, 1)
        print(self.text())

    @pyqtSlot()
    def on_replaceAllButton_clicked(self):
        regex = self.makeRegex()
        self.__text = regex.sub(self.replaceLineEdit.text(), self.__text)
        print(self.text())

    def makeRegex(self):
        findText = self.findLineEdit.text()
        if self.syntaxComboBox.currentText() == "Literal":
            findText = re.escape(findText)
        flags = re.MULTILINE | re.DOTALL | re.UNICODE
        if not self.caseCheckBox.isChecked():
            flags |= re.IGNORECASE
        if self.wholeCheckBox.isChecked():
            findText = r"\b%s\b" % findText
        return re.compile(findText, flags)


if __name__ == "__main__":

    text = """US experience shows that, unlike traditional patents, software patents do not encourage innovation and R&D, quite the contrary. 
    In particular they hurt small and medium-sized enterprises and generally newcomers in the market.
    They will just weaken the market and increase spending on patents and litigation, at the expense of technological innovation and research.
    Especially dangerous are attempts to abuse the patent system by preventing interoperability as a means of avoiding competition with technological ability.
    --- Extract quoted from Linus Torvalds and Alan Cox's letter
    to the President of the European Parliament http://www.effi.org/patentit/patents_torvalds_cox.html"""

    app = QApplication(sys.argv)
    form = FindAndReplaceDlg(text)
    form.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")
