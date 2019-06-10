import os
import platform
import random
import subprocess
import sys
import xml.etree.ElementTree as ET
from enum import Enum
from xml.dom import minidom

import pandas
import xlsxwriter
from googletrans import Translator
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QTimer

from tools.android.ui import localize_ui, dlg_localize_type_ui

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


class LocalizeTypeDlg(QtWidgets.QDialog, dlg_localize_type_ui.Ui_Dialog):

    def __init__(self, parent=None):
        super(LocalizeTypeDlg, self).__init__(parent)
        self.setupUi(self)
        self.comboBox.addItem(LOCALIZE.EN.value)
        self.comboBox.addItem(LOCALIZE.VI.value)

    def getValue(self):
        return self.comboBox.currentText()


class LOCALIZE(Enum):
    ID = "id"
    EN = "en"
    VI = "vi"


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
        self.containExport.setVisible(False)
        self.typeExport = None
        self.actionOpen_Xml.triggered.connect(lambda: self.openFile(False))
        self.actionOpen_Excel.triggered.connect(lambda: self.openFile(True))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.translator = Translator()

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
        print(listData)
        if isExcel:
            self.exportExcel(listData, path)
        else:
            self.exportXml(listData, path)

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
        if LOCALIZE.ID.value in listData.keys():
            listId = listData.get(LOCALIZE.ID.value)
            listData.pop(LOCALIZE.ID.value)
            # print(listId)
            for key, value in listData.items():
                self.seperatefolderString(listId, key, value, path)
            openDiction(path)

    def seperatefolderString(self, listId, key, value, path):
        path = '/'.join([path, "values-%s" % key])
        if not os.path.exists(path):
            os.mkdir(path)
        print(path)
        path = path + "/strings.xml"
        data = ET.Element('resources')
        for index, item in enumerate(value):
            string = ET.SubElement(data, 'string')
            string.set("name", listId[index])
            string.text = item
        data = ET.tostring(data)
        with open(path, "wb") as file:
            file.write(data)

    def openFile(self, isExcel):
        print("Open File")
        file_dialog = QtWidgets.QFileDialog(self)
        # the name filters must be a list
        if isExcel:
            nameFilter = ["Excel files (*.xlsx)"]
            nameSelectFilter = "Excel files (*.xlsx)"
        else:
            nameFilter = ["Xml files (*.xml)"]
            nameSelectFilter = "XML files (*.xml)"
        file_dialog.setNameFilters(nameFilter)
        file_dialog.selectNameFilter(nameSelectFilter)
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
            else:
                df = pandas.read_excel(path)

                self.tableWidget.setColumnCount(len(df.columns))
                self.tableWidget.setRowCount(len(df.index))

                for i in range(len(df.index)):
                    for j in range(len(df.columns)):
                        self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(df.iat[i, j])))
                header = list(df)
                print(header)
                self.tableWidget.setHorizontalHeaderLabels(header)
                self.updateRadioButton(False)
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
        self.language = self.translator.detect(value)
        QTimer.singleShot(0, lambda: self.detectLanguageComplete(size, listName, listValue))

    def detectLanguageComplete(self, size, listName, listValue):
        print(self.language)
        self.language = self.language.lang
        print(self.language)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(size)
        col_header = [LOCALIZE.ID.value, self.language]
        self.tableWidget.setHorizontalHeaderLabels(col_header)
        if listName.__len__() == listValue.__len__():
            for index in range(0, listName.__len__() - 1):
                self.tableWidget.setItem(index, 0, QtWidgets.QTableWidgetItem(listName[index]))
                self.tableWidget.setItem(index, 1, QtWidgets.QTableWidgetItem(listValue[index]))
        self.updateRadioButton(True)
        self.containExport.setVisible(True)

    def updateRadioButton(self, isExcel):
        if isExcel:
            self.rbExcel.setChecked(False)
            self.rbXml.setChecked(True)
        else:
            self.rbExcel.setChecked(True)
            self.rbXml.setChecked(False)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = Localize()
    main.show()
    sys.exit(app.exec_())
