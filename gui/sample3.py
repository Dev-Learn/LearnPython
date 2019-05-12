import sys
from decimal import Decimal
from urllib.request import urlopen

from PyQt5.QtWidgets import *


class Form(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        date = self.get_data()
        self.currencies = sorted(self.cur_code)
        dateLable = QLabel(date)
        self.fromCombobox = QComboBox()
        self.fromCombobox.addItems(self.currencies)
        self.fromSpinBox = QDoubleSpinBox()
        self.fromSpinBox.setRange(0.01, 10000000.00)
        self.fromSpinBox.setValue(1.00)
        self.toComboBox = QComboBox()
        self.toComboBox.addItems(self.currencies)
        self.toLable = QLabel("1.00")

        grid = QGridLayout()
        grid.addWidget(dateLable, 0, 0)
        grid.addWidget(self.fromCombobox, 1, 0)
        grid.addWidget(self.fromSpinBox, 1, 1)
        grid.addWidget(self.toComboBox, 2, 0)
        grid.addWidget(self.toLable, 2, 1)
        self.setLayout(grid)

        self.fromCombobox.currentIndexChanged.connect(self.updateUI)
        self.toComboBox.currentIndexChanged.connect(self.updateUI)
        self.fromSpinBox.valueChanged.connect(self.updateUI)
        self.setWindowTitle("Currency Converter")

    def updateUI(self):
        try:
            to = self.toComboBox.currentText()
            from_ = self.fromCombobox.currentText()
            to_code = self.cur_code[to]
            from_code = self.cur_code[from_]
            to_amt = Decimal(self.rates[to_code])
            from_amt = Decimal(self.rates[from_code])
            amt = Decimal(self.fromSpinBox.value())
            amount = (from_amt / to_amt) * amt
            self.toLable.setText("%.02f" % amount)
        except Exception as e:
            print(e)

    def get_data(self):
        url = "https://www.bankofcanada.ca/valet/observations/group/FX_RATES_DAILY/csv?start_date=2017-01-03"
        self.cur_code = {"Canadian Dollar": "FXCADCAS"}
        try:
            file = urlopen(url)
            file_handler = []
            for row in file:
                file_handler.append(row.decode())
            print(file_handler)
            print(file_handler.__len__())

            for row in file_handler:
                if row.startswith("FX"):
                    line = row.split(",")
                    cur = line[2].split(" to")[0]
                    cur = cur[1:]
                    print(cur)
                    self.cur_code[cur.title()] = line[0]
                else:
                    continue
            print(self.cur_code)
            header_list = []
            notFound = True
            x = 0
            while notFound:
                if file_handler[x].startswith("date"):
                    header = file_handler[x].split(",")
                    for col in header:
                        header_list.append(col.strip())
                    notFound = False
                x += 1
            print(header_list)
            print(header_list.__len__())

            data = []
            for row in file_handler[x:]:
                if row.startswith("\n"):
                    break
                else:
                    data = row.split(",")
            print(data)
            print(data.__len__())

            i = 0
            self.rates = {"FXCADCAS": "1.0000"}
            for item in data:
                header = "".join(str(header_list[i]))
                self.rates[header] = item.strip()
                i += 1

            print(self.rates)

            date = self.rates["date"]
            return "Exchange Rate Date : %s" % date

        except Exception as e:
            print(e)
            return "Fail to download"
        finally:
            file.close()


app = QApplication(sys.argv)
form = Form()
form.show()
sys.exit(app.exec_())
