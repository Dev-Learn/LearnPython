import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import gui.mainWindow.qrc_resources


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.image = QImage()

        self.imageLable = QLabel()
        self.imageLable.setMinimumSize(500, 500)
        self.imageLable.setAlignment(Qt.AlignCenter)
        self.imageLable.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.setCentralWidget(self.imageLable)

        dockWidget = QDockWidget("Log", self)
        dockWidget.setObjectName("LogDockWidger")
        dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        self.logListWidget = QListWidget()
        dockWidget.setWidget(self.logListWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, dockWidget)

        self.sizeLable = QLabel()
        self.sizeLable.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.setSizeGripEnabled(False)
        status.addPermanentWidget(self.sizeLable)
        status.showMessage("Ready", 5000)

    #     Action
        fileNewAction = self.createAction("&New...", "filenew", QKeySequence.New, "Create an image file", listener=self.fileNew)
        fileOpenAction = self.createAction("&Open...", "fileopen", QKeySequence.Open, "Open an existing image file", listener=self.fileOpen)
        fileSaveAction = self.createAction("&Save...", "filesave", QKeySequence.Save, "Save the image", listener=self.fileSave)
        fileSaveAsAction = self.createAction("Save &As......", "filesaveas", QKeySequence.Save, "Save the image using a new name", listener=self.fileSaveAs)
        fileQuitAsAction = self.createAction("&Quit", "filequit", QKeySequence.Save, "Close the application", listener=self.close)
        editInvertAction = self.createAction("&Invert", "editinvert", "Ctrl+I", "Invert the image's colors", True, listener=self.editInvert, signal ="toggled")
        editSwapRedAndBlueAction = self.createAction("Sw&ap Red and Blue", "editswap", "Ctrl+A", "Swap the image's red and blue color components", True, listener=self.editSwapRedAndBlue, signal ="toggled")
        editZoomAction = self.createAction("&Zoom...", "editzoom", "Alt+Z", "Zoom the image", listener=self.editSwapRedAndBlue)

    def createAction(self, text, icon=None, shorcut=None, tip=None, checkable=False, listener=None, signal="triggered"):
        action = QAction()
        action.setText(text)
        if icon is not None:
            action.setIcon(icon)
        if shorcut is not None:
            action.setShortcut(shorcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if checkable:
            action.setCheckable(True)
        if listener is not None:
            getattr(action, signal).connect(listener)
        return action


    def fileNew(self):
        pass


    def fileOpen(self):
        pass


    def fileSave(self):
        pass


    def fileSaveAs(self):
        pass


    def editInvert(self):
        pass


    def editSwapRedAndBlue(self):
        pass

def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Qtrac Ltd.")
    app.setOrganizationDomain("qtrac.eu")
    app.setApplicationName("Image Changer")
    app.setWindowIcon(QIcon(":/icon.png"))
    form = MainWindow()
    form.show()
    app.exec_()


main()
