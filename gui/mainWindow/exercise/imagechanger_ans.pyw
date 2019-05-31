import sys
import platform

import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from gui.mainWindow import helpform, newimagedlg
import gui.mainWindow.qrc_resources
from gui.mainWindow.exercise import resizedlg

__version__ = "1.0.1"


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.dirty = False
        self.filename = None
        self.mirroredvertically = False
        self.mirroredhorizontally = False
        self.printer = None

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
        fileNewAction = self.createAction("&New...", "filenew", QKeySequence.New, "Create an image file",
                                          listener=self.fileNew)
        fileOpenAction = self.createAction("&Open...", "fileopen", QKeySequence.Open, "Open an existing image file",
                                           listener=self.fileOpen)
        fileSaveAction = self.createAction("&Save...", "filesave", QKeySequence.Save, "Save the image",
                                           listener=self.fileSave)
        fileSaveAsAction = self.createAction("Save &As......", "filesaveas", QKeySequence.Save,
                                             "Save the image using a new name", listener=self.fileSaveAs)
        fileQuitAction = self.createAction("&Quit", "filequit", QKeySequence.Save, "Close the application",
                                           listener=self.close)

        editResizeAction = self.createAction("&Resize...", "editresize", "Ctrl+R", "Resize image",
                                             listener=self.editResize)
        editInvertAction = self.createAction("&Invert", "editinvert", "Ctrl+I", "Invert the image's colors", True,
                                             listener=self.editInvert, signal="toggled")
        editSwapRedAndBlueAction = self.createAction("Sw&ap Red and Blue", "editswap", "Ctrl+A",
                                                     "Swap the image's red and blue color components", True,
                                                     listener=self.editSwapRedAndBlue, signal="toggled")
        editZoomAction = self.createAction("&Zoom...", "editzoom", "Alt+Z", "Zoom the image",
                                           listener=self.editSwapRedAndBlue)
        editUnMirrorAction = self.createAction("&Unmirror", "editunmirror", "Ctrl+U", "Unmirror the image", True,
                                               listener=self.editUnMirror, signal="toggled")
        editMirrorHorizontalAction = self.createAction("Mirror &Horizontally", "editmirrorhoriz", "Ctrl+H",
                                                       "Horizontally mirror the image", True,
                                                       listener=self.editMirrorHorizontal, signal="toggled")
        editMirrorVerticalAction = self.createAction("Mirror &Vertically", "editmirrorvert", "Ctrl+V",
                                                     "Vertically mirror the image", True,
                                                     listener=self.editMirrorHorizontal, signal="toggled")
        helpAboutAction = self.createAction("&About Image Changer", listener=self.helpAbout)
        helpHelpAction = self.createAction("&Help", shorcut=QKeySequence.HelpContents, listener=self.helpHelp)

        mirrorGroup = QActionGroup(self)
        mirrorGroup.addAction(editUnMirrorAction)
        mirrorGroup.addAction(editMirrorHorizontalAction)
        mirrorGroup.addAction(editMirrorVerticalAction)

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenuActions = (
            fileNewAction,
            fileOpenAction,
            fileSaveAction,
            fileSaveAsAction,
            None,
            fileQuitAction)

        self.fileMenu.aboutToShow.connect(self.updateFileMenu)

        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (editInvertAction, editSwapRedAndBlueAction, editZoomAction))
        mirrorMenu = editMenu.addMenu(QIcon(":/editmirror.png"), "&Mirror")
        self.addActions(mirrorMenu, (editUnMirrorAction, editMirrorHorizontalAction, editMirrorVerticalAction))
        helpMenu = self.menuBar().addMenu("&Help")
        self.addActions(helpMenu, (helpAboutAction, helpHelpAction))

        fileToolBar = self.addToolBar("File")
        fileToolBar.setObjectName("FileToolBar")
        self.addActions(fileToolBar, (fileNewAction, fileOpenAction, fileSaveAction))
        editToolBar = self.addToolBar("Edit")
        editToolBar.setObjectName("EditToolBar")
        self.addActions(editToolBar, (
            editResizeAction, editInvertAction, editSwapRedAndBlueAction, editUnMirrorAction,
            editMirrorHorizontalAction,
            editMirrorVerticalAction))
        self.zoomSpinBox = QSpinBox()
        self.zoomSpinBox.setRange(1, 400)
        self.zoomSpinBox.setSuffix(" %")
        self.zoomSpinBox.setValue(100)
        self.zoomSpinBox.setToolTip("Zoom the Image")
        self.zoomSpinBox.setStatusTip(self.zoomSpinBox.toolTip())
        self.zoomSpinBox.setFocusPolicy(Qt.NoFocus)

        self.zoomSpinBox.valueChanged[int].connect(self.showImage)
        editToolBar.addWidget(self.zoomSpinBox)

        settings = QSettings()
        self.recentFiles = settings.value("RecentFiles") or []
        self.restoreGeometry(settings.value("MainWindow/Geometry", QByteArray()))
        self.restoreState(settings.value("MainWindow/State", QByteArray()))
        self.setWindowTitle("Image Changer")
        self.updateFileMenu()

        self.resetableActions = ((editInvertAction, False),
                                 (editSwapRedAndBlueAction, False),
                                 (editUnMirrorAction, True))

        QTimer.singleShot(0, self.loadInitialFile)

    def createAction(self, text, icon=None, shorcut=None, tip=None, checkable=False, listener=None, signal="triggered"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/{}.png".format(icon)))
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

    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def fileNew(self):
        if not self.okToContinue():
            return
        dialog = newimagedlg.NewImageDlg(self)
        if dialog.exec_():
            # self.addRecentFile(self.filename)
            self.image = QImage()
            for action, check in self.resetableActions:
                action.setChecked(check)
            self.image = dialog.image()
            self.filename = None
            self.dirty = True
            self.showImage()
            self.sizeLable.setText("{} x {}".format(
                self.image.width(), self.image.height()))
            self.updateStatus("Created new image")

    def fileOpen(self):
        pass

    def fileSave(self):
        pass

    def fileSaveAs(self):
        pass

    def editResize(self):
        print("Resize Image")
        if self.image.isNull():
            return

        form = resizedlg.ResizeDlg(self.image.width(), self.image.height())
        if form.exec_():
            width, height = form.result()
            if (
                            width == self.image.width() and
                            height == self.image.height()
            ):
                self.statusBar().showMessage("Resized to the same size",
                                             5000)
            else:
                self.image = self.image.scaled(width, height)
                self.showImage()
                self.dirty = True
                size = "{} x {}".format(
                    self.image.width(), self.image.height())
                self.sizeLable.setText(size)
                self.updateStatus("Resized to {}".format(size))

    def editInvert(self):
        pass

    def editSwapRedAndBlue(self):
        pass

    def editUnMirror(self):
        pass

    def editMirrorHorizontal(self):
        pass

    def helpAbout(self):
        QMessageBox.about(
            self,
            "About Image Changer",
            """<b>Image Changer</b> v {0}
            <p>Copyright &copy; 2008-10 Qtrac Ltd.
            All rights reserved.
            <p>This application can be used to perform
            simple image manipulations.
            <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(
                __version__, platform.python_version(),
                QT_VERSION_STR, PYQT_VERSION_STR,
                platform.system()))

    def helpHelp(self):
        form = helpform.HelpForm("index.html", self)
        form.show()

    def loadInitialFile(self):
        pass

    def updateFileMenu(self):
        pass

    def showImage(self):
        if self.image.isNull():
            return
        factor = self.zoomSpinBox.value() / 100.0
        width = self.image.width() * factor
        height = self.image.height() * factor
        image = self.image.scaled(width, height, Qt.KeepAspectRatio)
        self.imageLable.setPixmap(QPixmap.fromImage(image))

    def okToContinue(self):
        if self.dirty:
            reply = QMessageBox.question(
                self,
                "Image Changer - Unsaved Changes",
                "Save unsaved changes?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                return self.fileSave()
        return True

    def updateStatus(self, message):
        self.statusBar().showMessage(message, 5000)
        self.logListWidget.addItem(message)
        if self.filename:
            self.setWindowTitle("Image Changer - {}[*]".format(
                os.path.basename(self.filename)))
        elif not self.image.isNull():
            self.setWindowTitle("Image Changer - Unnamed[*]")
        else:
            self.setWindowTitle("Image Changer[*]")
        self.setWindowModified(self.dirty)


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
