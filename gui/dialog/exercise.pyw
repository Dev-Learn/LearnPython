import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


class FruitDlg(QDialog):
    def __init__(self, fruit, parent=None):
        super(FruitDlg, self).__init__(parent)
        self.input = fruit

        if fruit:
            title = "Edit Fruit"
            self.isAdd = False
        else:
            title = "Add Fruit"
            self.isAdd = True

        lableTitle = QLabel(title)
        self.inputLable = QLineEdit()
        if fruit:
            self.inputLable.setText(fruit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout = QGridLayout()
        layout.addWidget(lableTitle, 0, 0)
        layout.addWidget(self.inputLable, 1, 0)
        layout.addWidget(button_box, 2, 0)
        self.setLayout(layout)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        self.setWindowTitle(title)

    def accept(self):
        text = self.getText()
        if text:
            QDialog.accept(self)
        else:
            QMessageBox().warning(self, "Error", "Invalid Input")
            if self.input:
                self.inputLable.setText(self.input)
                self.inputLable.setCursorPosition(len(self.input))
                self.inputLable.setFocus()

    def getText(self):
        return self.inputLable.text()


class StringListDlg(QDialog):
    def __init__(self, fruits, parent=None):
        super(StringListDlg, self).__init__(parent)
        self.listWidget = QListWidget()
        self.listWidget.addItems(fruits)
        self.listWidget.setCurrentRow(0)
        buttonLayout = QVBoxLayout()

        addButton = QPushButton("Add Item")
        editButton = QPushButton("Edit Item")
        removeButton = QPushButton("Remove Item")
        upButton = QPushButton("Up")
        downButton = QPushButton("Down")
        sortButton = QPushButton("Sort Item")
        closeButton = QPushButton("Close Item")

        buttonLayout.addWidget(addButton)
        buttonLayout.addWidget(editButton)
        buttonLayout.addWidget(removeButton)
        buttonLayout.addWidget(upButton)
        buttonLayout.addWidget(downButton)
        buttonLayout.addWidget(sortButton)
        buttonLayout.addWidget(closeButton)

        layout = QHBoxLayout()
        layout.addWidget(self.listWidget)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        closeButton.clicked.connect(self.close)
        addButton.clicked.connect(lambda: self.interactiveFruit(None))
        editButton.clicked.connect(lambda: self.interactiveFruit(self.listWidget.currentItem()))
        removeButton.clicked.connect(lambda: self.removeItem())
        upButton.clicked.connect(lambda: self.move(False))
        downButton.clicked.connect(lambda: self.move())
        sortButton.clicked.connect(lambda: self.sort())

    def interactiveFruit(self, item):
        print(item)
        if item:
            dialog = FruitDlg(item.text(), self)
        else:
            dialog = FruitDlg(None, self)
        if dialog.exec_():
            print("aaa")
            text = dialog.getText()
            print(text)
            if dialog.isAdd:
                count = self.listWidget.__len__()
                item = QListWidgetItem(text)
                self.listWidget.insertItem(count, item)
                self.listWidget.setCurrentRow(count)
            else:
                item = self.listWidget.currentItem()
                item.setText(text)

    def removeItem(self):
        listItems = self.listWidget.selectedItems()
        if not listItems: return
        for item in listItems:
            self.listWidget.takeItem(self.listWidget.row(item))

    def move(self, isDown=True):
        itemCurrent = self.listWidget.currentItem()
        index = self.listWidget.row(itemCurrent)
        if isDown:
            position = index + 1
        else:
            position = index - 1
        if position != -1 and position < self.listWidget.__len__():
            temp = self.listWidget.takeItem(position)
            self.listWidget.insertItem(index, temp)
            self.listWidget.insertItem(position, itemCurrent)

    def sort(self):
        self.listWidget.sortItems(Qt.AscendingOrder)


if __name__ == "__main__":
    fruits = ["Banana", "Apple", "Elderberry", "Clementine", "Fig", "Guava", "Mango", "Honeydew Melon", "Date",
              "Watermelon", "Tangerine", "Ugli Fruit", "Juniperberry", "Kiwi", "Lemon", "Nectarine", "Plum",
              "Raspberry",
              "Strawberry", "Orange"]
    app = QApplication(sys.argv)
    form = StringListDlg(fruits)
    form.show()
    sys.exit(app.exec_())
