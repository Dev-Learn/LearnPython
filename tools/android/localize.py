import sys

import pandas

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot

from tools.android.ui import localize_ui
from xml.dom import minidom


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

    @pyqtSlot()
    def on_btExport_clicked(self):
        isExcel = self.rbExcel.isChecked()
        if isExcel:
            nameFilter = "*.xlsx"
        else:
            nameFilter = "*.xml"
        fdialog = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Image As', nameFilter)
        fname = fdialog[0]
        if fname:
            print(fname)
            # self.export(isExcel)

    def export(self, isExcel):
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
            self.exportExcel(listData)
        else:
            self.exportXml(listData)

    def exportExcel(self, listData):
        pass

    def exportXml(self, listData):
        pass

    def openFile(self, isExcel):
        print("Open File")
        file_dialog = QtWidgets.QFileDialog(self)
        # the name filters must be a list
        if isExcel:
            nameFilter = ["Excel files (*.xlsx)"]
            nameSelectFilter = "Excel files (*.xlsx)"
        else:
            nameFilter = ["Text files (*.txt)","Xml files (*.xml)"]
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
                if name == "strings.xml":
                    doc = minidom.parse(path)
                    items = doc.getElementsByTagName('string')
                    size = items.length
                    print(size)
                    self.tableWidget.setColumnCount(2)
                    self.tableWidget.setRowCount(size)
                    col_header = ["Id", "En"]
                    self.tableWidget.setHorizontalHeaderLabels(col_header)
                    listName = []
                    listValue = []
                    for item in items:
                        listName.append(item.attributes['name'].value)
                        data = item.firstChild
                        listValue.append(data.data if data else '')
                    if listName.__len__() == listValue.__len__():
                        for index in range(0, listName.__len__() - 1):
                            self.tableWidget.setItem(index, 0, QtWidgets.QTableWidgetItem(listName[index]))
                            self.tableWidget.setItem(index, 1, QtWidgets.QTableWidgetItem(listValue[index]))
                    self.updateRadioButton(True)
                else:
                    QtWidgets.QMessageBox().warning(self, "Error", "Please choose file string")
                    self.openFile()
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

    def updateRadioButton(self, isString):
        if isString:
            self.rbExcel.setChecked(True)
            self.rbXml.setChecked(False)
        else:
            self.rbExcel.setChecked(False)
            self.rbXml.setChecked(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = Localize()
    main.show()
    sys.exit(app.exec_())
