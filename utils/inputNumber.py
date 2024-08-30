from PyQt5.QtWidgets import QLabel, QHBoxLayout, QLineEdit, QPushButton

class InputNumber(QLabel):
    def __init__(self, defaultNumber = 0, parent = None):
        super().__init__(parent)

        self.defaultNumber = defaultNumber

        layout = QHBoxLayout(self)
        self.inputNum = QLineEdit(self)
        self.inputNum.setText(str(defaultNumber))
        self.inputNum.setReadOnly(True)

        addNumber = QPushButton("↑", self)
        addNumber.clicked.connect(self.addNum)

        restNumber = QPushButton("↓", self)
        restNumber.clicked.connect(self.restNum)

        layout.addWidget(addNumber)
        layout.addWidget(self.inputNum)
        layout.addWidget(restNumber)

        layout.setSpacing(0)
    
    def addNum(self):
        actualNum = self.inputNum.text()
        self.inputNum.setText(str(int(actualNum) + 1))

    def restNum(self):
        actualNum = self.inputNum.text()
    
        if int(actualNum) > self.defaultNumber:
            self.inputNum.setText(str(int(actualNum) - 1))
