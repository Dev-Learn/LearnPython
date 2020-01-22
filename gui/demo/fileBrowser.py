import sys

import subprocess, os, platform

import os
from PyQt5 import QtWidgets, QtCore, QtGui
from gui.demo import demo_ui


class FileBrowser(demo_ui.Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super(FileBrowser, self).__init__()
        self.setupUi(self)
        self.fileBrower.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.fileBrower.customContextMenuRequested.connect(self.context_menu)
        self.populate()

    def populate(self):
        path = "/Users/trannam"
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.fileBrower.setModel(self.model)
        self.fileBrower.setRootIndex(self.model.index(path))
        self.fileBrower.setSortingEnabled(True)

    def context_menu(self):
        menu = QtWidgets.QMenu()
        open = menu.addAction("Open")
        open.triggered.connect(self.openFile)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def openFile(self):
        index = self.fileBrower.currentIndex()
        path = self.model.filePath(index)
        name = self.model.fileName(index)
        print(path)
        print(name)
        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', path))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(path)
        else:  # linux variants
            subprocess.call(('xdg-open', path))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    fileBrowser = FileBrowser()
    fileBrowser.show()
    sys.exit(app.exec_())
