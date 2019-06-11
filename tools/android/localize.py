import codecs
import json
import os
import platform
import random
import subprocess
import sys
from functools import partial
from xml.dom import minidom

import pandas
import xlsxwriter
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QThread
from lxml import etree

# module_path = os.path.abspath(os.getcwd())
#
# if module_path not in sys.path:
#     print("%s" % module_path)
#     sys.path.append(module_path)

# Back up the reference to the exceptionhook
from tools.android import worker
from tools.android.ui import dlg_localize_type_ui, localize_ui

sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

ID = "id"


class LocalizeTypeDlg(QtWidgets.QDialog, dlg_localize_type_ui.Ui_Dialog):
    def __init__(self, listLanguage, parent=None):
        super(LocalizeTypeDlg, self).__init__(parent)
        self.setupUi(self)
        data = json.load(codecs.open("Language_Country.json", mode='r', encoding="utf8"))
        print(data)
        for item in data:
            code = item["Language_Code"]
            if code not in listLanguage:
                self.comboBox.addItem(item["Name"], code)

    def getValue(self):
        return self.comboBox.currentData()

    def getName(self):
        return self.comboBox.currentText()


def getRow(index, isValue=False):
    global row
    if index == 0:
        row = "A"
    elif index == 1:
        row = "B"
    elif index == 2:
        row = "C"
    elif index == 3:
        row = "D"
    elif index == 4:
        row = "E"
    elif index == 5:
        row = "F"
    elif index == 6:
        row = "G"
    elif index == 7:
        row = "H"
    elif index == 8:
        row = "K"
    elif index == 9:
        row = "L"
    elif index == 10:
        row = "M"
    if isValue:
        return row + str(2)
    else:
        return row + str(1)


def openDiction(path):
    print(path)
    if not os.path.isdir(path):
        file = path.split("/")[-1]
        path = path.replace(file, "")

    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', path))
    elif platform.system() == 'Windows':  # Windows
        os.startfile(path)
    else:  # linux variants
        subprocess.call(('xdg-open', path))


class Localize(localize_ui.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(Localize, self).__init__()
        self.setupUi(self)
        self.columnCount = 2
        self.header = []
        self.containExport.setVisible(False)
        self.typeExport = None
        self.actionOpen.triggered.connect(self.openFile)
        self.actionAddLanguage.triggered.connect(self.addMoreLanguage)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

    def addMoreLanguage(self):
        if not self.header:
            QtWidgets.QMessageBox().warning(self, "Error", "Please import xml or xlsx file")
            return
        dialog = LocalizeTypeDlg(self.header)
        if dialog.exec_():
            name = dialog.getName()
            code = dialog.getValue()
            print(code)
            listData = self.getDataFromTable()
            print(listData)
            listData.pop(ID.value)
            listResource = listData.get(random.choice(list(listData.keys())))
            print(listResource)
            self.columnCount = self.tableWidget.columnCount()
            print(self.columnCount)
            self.tableWidget.insertColumn(self.columnCount)
            self.header.append(code)
            print(self.header)
            self.tableWidget.setHorizontalHeaderLabels(self.header)
            self.showLogStatusBar("Translate Language to %s..." % name)
            obj = worker.WorkerTranslate(translateLanguage={"listResource": listResource, "code": code})
            thread = QThread(self)
            obj.translateComplete.connect(self.translateLanguageComplete)
            obj.translateStatus.connect(self.translateStatus)
            obj.translateError.connect(self.translateError)
            obj.moveToThread(thread)
            thread.started.connect(partial(obj.translateLanguage))
            thread.start()

    @pyqtSlot(str, int)
    def translateLanguageComplete(self, translate, index):
        self.tableWidget.setItem(index, self.columnCount, QtWidgets.QTableWidgetItem(translate))

    @pyqtSlot(str, str)
    def translateStatus(self, currentText, transtateText):
        self.showLogStatusBar("%s transtate to -> %s" % (currentText, transtateText))

    @pyqtSlot()
    def translateError(self):
        self.tableWidget.removeColumn(self.columnCount)
        headerError = self.header[-1]
        self.header.remove(headerError)
        print(self.header)
        self.tableWidget.setHorizontalHeaderLabels(self.header)

    @pyqtSlot()
    def on_btExport_clicked(self):
        isExcel = self.rbExcel.isChecked()
        if isExcel:
            nameFilter = ".xlsx"
            fdialog = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', filter=nameFilter)
            path = fdialog[0]
            print(path)
        else:
            path = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
            print(path)

        if path:
            self.export(isExcel, path)

    def export(self, isExcel, path):
        listData = self.getDataFromTable()
        print(listData)
        if isExcel:
            self.exportExcel(listData, path)
        else:
            self.exportXml(listData, path)

    def getDataFromTable(self):
        listData = {}
        row = 0
        col = 0
        for i in range(self.tableWidget.columnCount()):
            list = []
            header = str(self.tableWidget.horizontalHeaderItem(col).text())
            # print(header)
            for x in range(self.tableWidget.rowCount()):
                try:
                    text = str(self.tableWidget.item(row, col).text())
                    # print(text)
                    list.append(text)
                    row += 1
                except AttributeError:
                    row += 1
            # print(list)
            listData[header] = list
            row = 0
            col += 1
        return listData

    def exportExcel(self, listData, path):
        workbook = xlsxwriter.Workbook(path + ".xlsx")
        worksheet = workbook.add_worksheet()
        index = 0
        for key, value in listData.items():
            rowKey = getRow(index)
            print(rowKey)
            print(key)
            worksheet.write(rowKey, key)
            rowValue = getRow(index, True)
            print(rowValue)
            worksheet.write_column(rowValue, value)
            index += 1
        workbook.close()

        QtWidgets.QMessageBox().information(self, "Success", "Export file excel success")
        openDiction(path)

    def exportXml(self, listData, path):
        if ID in listData.keys():
            listId = listData.get(ID)
            listData.pop(ID)
            # print(listId)
            for key, value in listData.items():
                self.seperateFolderString(listId, key, value, path)
            openDiction(path)

    def seperateFolderString(self, listId, key, value, path):
        path = '/'.join([path, "values-%s" % key])
        if not os.path.exists(path):
            os.mkdir(path)
        print(path)
        path = path + "/strings.xml"
        root = etree.Element('resources')
        for index, item in enumerate(value):
            child = etree.Element('string')
            child.set('name', listId[index])
            child.text = item
            root.append(child)
            # string = ET.SubElement(data, 'string')
            # string.set("name", listId[index])
            # string.text = item
        # data = ET.tostring(data)
        data = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True)
        print(data)
        with open(path, "wb") as file:
            file.write(data)

    def openFile(self, isExcel):
        print("Open File")
        file_dialog = QtWidgets.QFileDialog(self)
        # the name filters must be a list
        file_dialog.setNameFilters(["Xml files (*.xml)", "Excel files (*.xlsx)"])
        # show the dialog
        if file_dialog.exec_():
            path = file_dialog.selectedFiles()[0]
            name = path.split("/")[-1]
            print(name)
            print(path)
            if ".xml" in name:
                doc = minidom.parse(path)
                items = doc.getElementsByTagName('string')
                if items:
                    self.detectLanguage(items)
                else:
                    QtWidgets.QMessageBox().warning(self, "Error", "Please choose file string")
                    self.openFile(isExcel)
                return
            elif ".xlsx" in name:
                df = pandas.read_excel(path)

                self.columnCount = len(df.columns)
                self.tableWidget.setColumnCount(self.columnCount)
                self.tableWidget.setRowCount(len(df.index))

                for i in range(len(df.index)):
                    for j in range(len(df.columns)):
                        self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(df.iat[i, j])))
                self.header = list(df)
                print(self.header)
                self.tableWidget.setHorizontalHeaderLabels(self.header)
                self.updateRadioButton(True)
            else:
                QtWidgets.QMessageBox().warning(self, "Error", "Please choose file xml or xlsx")
                self.openFile(isExcel)
            self.containExport.setVisible(True)

    def detectLanguage(self, items):
        size = items.length
        print(size)
        listName = []
        listValue = []
        for item in items:
            listName.append(item.attributes['name'].value)
            data = item.firstChild
            listValue.append(data.data if data else '')
        value = random.choice(listValue)
        obj = worker.WorkerTranslate(detectLanguage={"text": value, "size": size, "listName": listName,
                                                     "listValue": listValue})
        self.showLogStatusBar("Detect Language ...")
        thread = QThread(self)
        obj.detectComplete.connect(self.detectLanguageComplete)
        obj.moveToThread(thread)
        thread.started.connect(partial(obj.detectLanguage))
        thread.start()

    @pyqtSlot(str, int, list, list)
    def detectLanguageComplete(self, languagecode, size, listName, listValue):
        self.showLogStatusBar("Detect Language Complete : %s..." % languagecode)
        print(languagecode)
        self.tableWidget.setColumnCount(self.columnCount)
        self.tableWidget.setRowCount(size)
        self.header = [ID, languagecode]
        self.tableWidget.setHorizontalHeaderLabels(self.header)
        if listName.__len__() == listValue.__len__():
            for index in range(0, listName.__len__() - 1):
                self.tableWidget.setItem(index, 0, QtWidgets.QTableWidgetItem(listName[index]))
                self.tableWidget.setItem(index, 1, QtWidgets.QTableWidgetItem(listValue[index]))
        self.updateRadioButton(False)
        self.containExport.setVisible(True)

    def updateRadioButton(self, isExcel):
        if isExcel:
            self.rbExcel.setChecked(False)
            self.rbXml.setChecked(True)
        else:
            self.rbExcel.setChecked(True)
            self.rbXml.setChecked(False)

    def showLogStatusBar(self, message):
        self.statusBar().showMessage(message, 5000)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = Localize()
    main.raise_()
    main.show()
    sys.exit(app.exec_())
