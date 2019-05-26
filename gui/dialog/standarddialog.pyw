import math
import random
import string
import sys

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import *


class NumberFormatDlg(QDialog):
    def __init__(self, format, parent=None):
        super(NumberFormatDlg, self).__init__(parent)
        thousands_label = QLabel("&Thousands separator")
        self.thousandsEdit = QLineEdit(format["thousandsseparator"])
        thousands_label.setBuddy(self.thousandsEdit)
        decimal_marker_label = QLabel("Decimal &marker")
        self.decimalMarkerEdit = QLineEdit(format["decimalmarker"])
        decimal_marker_label.setBuddy(self.decimalMarkerEdit)
        decimal_places_label = QLabel("&Decimal places")
        self.decimalPlacesSpinBox = QSpinBox()
        decimal_places_label.setBuddy(self.decimalPlacesSpinBox)
        self.decimalPlacesSpinBox.setRange(0, 6)
        self.decimalPlacesSpinBox.setValue(format["decimalplaces"])
        self.redNegativesCheckBox = QCheckBox("&Red negative numbers")
        self.redNegativesCheckBox.setChecked(format["rednegatives"])
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.format = format.copy()
        grid = QGridLayout()
        grid.addWidget(thousands_label, 0, 0)
        grid.addWidget(self.thousandsEdit, 0, 1)
        grid.addWidget(decimal_marker_label, 1, 0)
        grid.addWidget(self.decimalMarkerEdit, 1, 1)
        grid.addWidget(decimal_places_label, 2, 0)
        grid.addWidget(self.decimalPlacesSpinBox, 2, 1)
        grid.addWidget(self.redNegativesCheckBox, 3, 0, 1, 2)
        grid.addWidget(button_box, 4, 0, 1, 2)
        self.setLayout(grid)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.setWindowTitle("Set Number Format (Modal)")

    def accept(self):
        class ThousandsError(Exception):
            pass

        class DecimalError(Exception):
            pass

        punctuation = frozenset(" ,;:.")

        thousands = self.thousandsEdit.text()
        decimal = self.decimalMarkerEdit.text()
        try:
            if len(decimal) == 0:
                raise DecimalError("The decimal marker may not be "
                                   "empty.")
            if len(thousands) > 1:
                raise ThousandsError("The thousands separator may "
                                     "only be empty or one character.")
            if len(decimal) > 1:
                raise DecimalError("The decimal marker must be "
                                   "one character.")
            if thousands == decimal:
                raise ThousandsError("The thousands separator and "
                                     "the decimal marker must be different.")
            if thousands and thousands not in punctuation:
                raise ThousandsError("The thousands separator must "
                                     "be a punctuation symbol.")
            if decimal not in punctuation:
                raise DecimalError("The decimal marker must be a "
                                   "punctuation symbol.")
        except ThousandsError as e:
            QMessageBox().warning(self, "Thousands Separator Error",
                                  str(e))
            self.thousandsEdit.selectAll()
            self.thousandsEdit.setFocus()
            return
        except DecimalError as e:
            QMessageBox().warning(self, "Decimal Marker Error",
                                  str(e))
            self.decimalMarkerEdit.selectAll()
            self.decimalMarkerEdit.setFocus()
            return

        self.format["thousandsseparator"] = thousands
        self.format["decimalmarker"] = decimal
        self.format["decimalplaces"] = self.decimalPlacesSpinBox.value()
        self.format["rednegatives"] = self.redNegativesCheckBox.isChecked()
        QDialog.accept(self)

    def numberFormat(self):
        return self.format


class Form(QDialog):
    X_MAX = 26
    Y_MAX = 60

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.numberFormatDlg = None
        self.format = dict(thousandsseparator=",",
                           decimalmarker=".", decimalplaces=2,
                           rednegatives=False)
        self.numbers = {}
        for x in range(self.X_MAX):
            for y in range(self.Y_MAX):
                self.numbers[(x, y)] = (10000 * random.random()) - 5000

        self.table = QTableWidget()
        format_button = QPushButton("Set Number Format... "
                                     "(&Modal)")

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(format_button)
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        format_button.clicked.connect(self.setNumberFormat)

        self.setWindowTitle("Numbers")
        self.refreshTable()

    def refreshTable(self):
        self.table.clear()
        self.table.setColumnCount(self.X_MAX)
        self.table.setRowCount(self.Y_MAX)
        self.table.setHorizontalHeaderLabels(
            list(string.ascii_uppercase))
        for x in range(self.X_MAX):
            for y in range(self.Y_MAX):
                fraction, whole = math.modf(self.numbers[(x, y)])
                sign = "-" if whole < 0 else ""
                whole = "%d" % math.floor(abs(whole))
                digits = []
                for i, digit in enumerate(reversed(whole)):
                    if i and i % 3 == 0:
                        digits.insert(0, self.format["thousandsseparator"])
                    digits.insert(0, digit)
                if self.format["decimalplaces"]:
                    fraction = "%0.7f" % abs(fraction)
                    fraction = (self.format["decimalmarker"] +
                                fraction[2:self.format["decimalplaces"]
                                           + 2])
                else:
                    fraction = ""
                text = "%s%s%s" % (sign, "".join(digits), fraction)
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                if sign and self.format["rednegatives"]:
                    item.setBackground(Qt.red)
                self.table.setItem(y, x, item)

    def setNumberFormat(self):
        dialog = NumberFormatDlg(self.format, self)
        if dialog.exec_():
            self.format = dialog.numberFormat()
            self.refreshTable()


app = QApplication(sys.argv)
form = Form()
form.show()
sys.exit(app.exec_())
