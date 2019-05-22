import sys
from PyQt5.QtWidgets import *


class Form(QDialog):
    def __init__(self):
        super().__init__()

        principalTitle = QLabel()
        principalTitle.setText("Principal:")

        rateTitle = QLabel()
        rateTitle.setText("Rate:")

        yearTitle = QLabel()
        yearTitle.setText("Years:")

        amountTitle = QLabel()
        amountTitle.setText("Amount")

        self.principalSpinBox = QDoubleSpinBox()
        self.principalSpinBox.setPrefix("$ ")
        self.principalSpinBox.setRange(1.00, 10000.00)
        self.principalSpinBox.valueChanged.connect(self.updateUI)

        self.rateSpinBox = QDoubleSpinBox()
        self.rateSpinBox.setPrefix("% ")
        self.rateSpinBox.setRange(0.01, 100.00)
        self.rateSpinBox.valueChanged.connect(self.updateUI)

        self.yearComboBox = QComboBox()
        self.yearComboBox.addItem("1 years")
        self.yearComboBox.addItem("2 years")
        self.yearComboBox.addItem("3 years")
        self.yearComboBox.currentIndexChanged.connect(self.updateUI)

        self.amountValue = QLabel()

        gridLayout = QGridLayout()
        gridLayout.addWidget(principalTitle, 0, 0)
        gridLayout.addWidget(self.principalSpinBox, 0, 1)
        gridLayout.addWidget(rateTitle, 1, 0)
        gridLayout.addWidget(self.rateSpinBox, 1, 1)
        gridLayout.addWidget(yearTitle, 2, 0)
        gridLayout.addWidget(self.yearComboBox, 2, 1)
        gridLayout.addWidget(amountTitle, 3, 0)
        gridLayout.addWidget(self.amountValue, 3, 1)
        self.setLayout(gridLayout)
        self.updateUI()

    def updateUI(self):
        principal = self.principalSpinBox.value()
        rate = self.rateSpinBox.value()
        yearText = self.yearComboBox.currentText()
        years = int(yearText.replace(" years", ""))
        amount = principal * ((1 + (rate / 100.0)) ** years)
        self.amountValue.setText(str("$ %.02f" % amount))


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
