from PyQt5.QtWidgets import QLabel, QHBoxLayout, QLineEdit, QPushButton

class InputNumber(QLabel):
    def __init__(self, defaultNumber = 0, parent = None):
        super().__init__(parent)

        self.defaultNumber = defaultNumber

        self.initUI()
        self.initEvents()
    
    def initUI(self):
        layout = QHBoxLayout(self)
        self.inputNum = QLineEdit(self)
        self.inputNum.setText(str(self.defaultNumber))
        self.inputNum.setReadOnly(True)

        self.addNumber = QPushButton("↑", self)

        self.restNumber = QPushButton("↓", self)

        layout.addWidget(self.addNumber)
        layout.addWidget(self.inputNum)
        layout.addWidget(self.restNumber)

        layout.setSpacing(0)
    
    def initEvents(self):
        self.addNumber.clicked.connect(self.addNum)
        self.restNumber.clicked.connect(self.restNum)

    def addNum(self):
        actualNum = self.inputNum.text()
        self.inputNum.setText(str(int(actualNum) + 1))

    def restNum(self):
        actualNum = self.inputNum.text()
    
        if int(actualNum) > self.defaultNumber:
            self.inputNum.setText(str(int(actualNum) - 1))

    def getNum(self):
        return int(self.inputNum.text())